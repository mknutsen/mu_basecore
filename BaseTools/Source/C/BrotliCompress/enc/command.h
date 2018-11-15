<<<<<<< HEAD
/* Copyright 2013 Google Inc. All Rights Reserved.

   Distributed under MIT license.
   See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
*/

/* This class models a sequence of literals and a backward reference copy. */

#ifndef BROTLI_ENC_COMMAND_H_
#define BROTLI_ENC_COMMAND_H_

#include "../common/types.h"
#include "../common/port.h"
#include "./fast_log.h"
#include "./prefix.h"

#if defined(__cplusplus) || defined(c_plusplus)
extern "C" {
#endif

static uint32_t kInsBase[] =   { 0, 1, 2, 3, 4, 5, 6, 8, 10, 14, 18, 26, 34, 50,
    66, 98, 130, 194, 322, 578, 1090, 2114, 6210, 22594 };
static uint32_t kInsExtra[] =  { 0, 0, 0, 0, 0, 0, 1, 1,  2,  2,  3,  3,  4,  4,
    5,   5,   6,   7,   8,   9,   10,   12,   14,    24 };
static uint32_t kCopyBase[] =  { 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 18, 22, 30,
    38, 54,  70, 102, 134, 198, 326,   582, 1094,  2118 };
static uint32_t kCopyExtra[] = { 0, 0, 0, 0, 0, 0, 0, 0,  1,  1,  2,  2,  3,  3,
     4,  4,   5,   5,   6,   7,   8,     9,   10,    24 };

static BROTLI_INLINE uint16_t GetInsertLengthCode(size_t insertlen) {
  if (insertlen < 6) {
    return (uint16_t)insertlen;
  } else if (insertlen < 130) {
    uint32_t nbits = Log2FloorNonZero(insertlen - 2) - 1u;
    return (uint16_t)((nbits << 1) + ((insertlen - 2) >> nbits) + 2);
  } else if (insertlen < 2114) {
    return (uint16_t)(Log2FloorNonZero(insertlen - 66) + 10);
  } else if (insertlen < 6210) {
    return 21u;
  } else if (insertlen < 22594) {
    return 22u;
  } else {
    return 23u;
  }
}

static BROTLI_INLINE uint16_t GetCopyLengthCode(size_t copylen) {
  if (copylen < 10) {
    return (uint16_t)(copylen - 2);
  } else if (copylen < 134) {
    uint32_t nbits = Log2FloorNonZero(copylen - 6) - 1u;
    return (uint16_t)((nbits << 1) + ((copylen - 6) >> nbits) + 4);
  } else if (copylen < 2118) {
    return (uint16_t)(Log2FloorNonZero(copylen - 70) + 12);
  } else {
    return 23u;
  }
}

static BROTLI_INLINE uint16_t CombineLengthCodes(
    uint16_t inscode, uint16_t copycode, BROTLI_BOOL use_last_distance) {
  uint16_t bits64 =
      (uint16_t)((copycode & 0x7u) | ((inscode & 0x7u) << 3));
  if (use_last_distance && inscode < 8 && copycode < 16) {
    return (copycode < 8) ? bits64 : (bits64 | 64);
  } else {
    /* "To convert an insert-and-copy length code to an insert length code and
       a copy length code, the following table can be used" */
    static const uint16_t cells[9] = { 128u, 192u, 384u, 256u, 320u, 512u,
                                       448u, 576u, 640u };
    return cells[(copycode >> 3) + 3 * (inscode >> 3)] | bits64;
  }
}

static BROTLI_INLINE void GetLengthCode(size_t insertlen, size_t copylen,
                                        BROTLI_BOOL use_last_distance,
                                        uint16_t* code) {
  uint16_t inscode = GetInsertLengthCode(insertlen);
  uint16_t copycode = GetCopyLengthCode(copylen);
  *code = CombineLengthCodes(inscode, copycode, use_last_distance);
}

static BROTLI_INLINE uint32_t GetInsertBase(uint16_t inscode) {
  return kInsBase[inscode];
}

static BROTLI_INLINE uint32_t GetInsertExtra(uint16_t inscode) {
  return kInsExtra[inscode];
}

static BROTLI_INLINE uint32_t GetCopyBase(uint16_t copycode) {
  return kCopyBase[copycode];
}

static BROTLI_INLINE uint32_t GetCopyExtra(uint16_t copycode) {
  return kCopyExtra[copycode];
}

typedef struct Command {
  uint32_t insert_len_;
  /* Stores copy_len in low 24 bits and copy_len XOR copy_code in high 8 bit. */
  uint32_t copy_len_;
  uint32_t dist_extra_;
  uint16_t cmd_prefix_;
  uint16_t dist_prefix_;
} Command;

/* distance_code is e.g. 0 for same-as-last short code, or 16 for offset 1. */
static BROTLI_INLINE void InitCommand(Command* self, size_t insertlen,
    size_t copylen, size_t copylen_code, size_t distance_code) {
  self->insert_len_ = (uint32_t)insertlen;
  self->copy_len_ = (uint32_t)(copylen | ((copylen_code ^ copylen) << 24));
  /* The distance prefix and extra bits are stored in this Command as if
     npostfix and ndirect were 0, they are only recomputed later after the
     clustering if needed. */
  PrefixEncodeCopyDistance(
      distance_code, 0, 0, &self->dist_prefix_, &self->dist_extra_);
  GetLengthCode(
      insertlen, copylen_code, TO_BROTLI_BOOL(self->dist_prefix_ == 0),
      &self->cmd_prefix_);
}

static BROTLI_INLINE void InitInsertCommand(Command* self, size_t insertlen) {
  self->insert_len_ = (uint32_t)insertlen;
  self->copy_len_ = 4 << 24;
  self->dist_extra_ = 0;
  self->dist_prefix_ = 16;
  GetLengthCode(insertlen, 4, BROTLI_FALSE, &self->cmd_prefix_);
}

static BROTLI_INLINE uint32_t CommandDistanceCode(const Command* self) {
  if (self->dist_prefix_ < 16) {
    return self->dist_prefix_;
  } else {
    uint32_t nbits = self->dist_extra_ >> 24;
    uint32_t extra = self->dist_extra_ & 0xffffff;
    uint32_t prefix = self->dist_prefix_ - 12u - 2u * nbits;
    return (prefix << nbits) + extra + 12;
  }
}

static BROTLI_INLINE uint32_t CommandDistanceContext(const Command* self) {
  uint32_t r = self->cmd_prefix_ >> 6;
  uint32_t c = self->cmd_prefix_ & 7;
  if ((r == 0 || r == 2 || r == 4 || r == 7) && (c <= 2)) {
    return c;
  }
  return 3;
}

static BROTLI_INLINE uint32_t CommandCopyLen(const Command* self) {
  return self->copy_len_ & 0xFFFFFF;
}

static BROTLI_INLINE uint32_t CommandCopyLenCode(const Command* self) {
  return (self->copy_len_ & 0xFFFFFF) ^ (self->copy_len_ >> 24);
}

#if defined(__cplusplus) || defined(c_plusplus)
}  /* extern "C" */
#endif

#endif  /* BROTLI_ENC_COMMAND_H_ */
=======
/* Copyright 2013 Google Inc. All Rights Reserved.

   Distributed under MIT license.
   See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
*/

/* This class models a sequence of literals and a backward reference copy. */

#ifndef BROTLI_ENC_COMMAND_H_
#define BROTLI_ENC_COMMAND_H_

#include "../common/constants.h"
#include "../common/platform.h"
#include <brotli/types.h>
#include "./fast_log.h"
#include "./params.h"
#include "./prefix.h"

#if defined(__cplusplus) || defined(c_plusplus)
extern "C" {
#endif

static uint32_t kInsBase[] =   { 0, 1, 2, 3, 4, 5, 6, 8, 10, 14, 18, 26, 34, 50,
    66, 98, 130, 194, 322, 578, 1090, 2114, 6210, 22594 };
static uint32_t kInsExtra[] =  { 0, 0, 0, 0, 0, 0, 1, 1,  2,  2,  3,  3,  4,  4,
    5,   5,   6,   7,   8,   9,   10,   12,   14,    24 };
static uint32_t kCopyBase[] =  { 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 18, 22, 30,
    38, 54,  70, 102, 134, 198, 326,   582, 1094,  2118 };
static uint32_t kCopyExtra[] = { 0, 0, 0, 0, 0, 0, 0, 0,  1,  1,  2,  2,  3,  3,
     4,  4,   5,   5,   6,   7,   8,     9,   10,    24 };

static BROTLI_INLINE uint16_t GetInsertLengthCode(size_t insertlen) {
  if (insertlen < 6) {
    return (uint16_t)insertlen;
  } else if (insertlen < 130) {
    uint32_t nbits = Log2FloorNonZero(insertlen - 2) - 1u;
    return (uint16_t)((nbits << 1) + ((insertlen - 2) >> nbits) + 2);
  } else if (insertlen < 2114) {
    return (uint16_t)(Log2FloorNonZero(insertlen - 66) + 10);
  } else if (insertlen < 6210) {
    return 21u;
  } else if (insertlen < 22594) {
    return 22u;
  } else {
    return 23u;
  }
}

static BROTLI_INLINE uint16_t GetCopyLengthCode(size_t copylen) {
  if (copylen < 10) {
    return (uint16_t)(copylen - 2);
  } else if (copylen < 134) {
    uint32_t nbits = Log2FloorNonZero(copylen - 6) - 1u;
    return (uint16_t)((nbits << 1) + ((copylen - 6) >> nbits) + 4);
  } else if (copylen < 2118) {
    return (uint16_t)(Log2FloorNonZero(copylen - 70) + 12);
  } else {
    return 23u;
  }
}

static BROTLI_INLINE uint16_t CombineLengthCodes(
    uint16_t inscode, uint16_t copycode, BROTLI_BOOL use_last_distance) {
  uint16_t bits64 =
      (uint16_t)((copycode & 0x7u) | ((inscode & 0x7u) << 3u));
  if (use_last_distance && inscode < 8u && copycode < 16u) {
    return (copycode < 8u) ? bits64 : (bits64 | 64u);
  } else {
    /* Specification: 5 Encoding of ... (last table) */
    /* offset = 2 * index, where index is in range [0..8] */
    uint32_t offset = 2u * ((copycode >> 3u) + 3u * (inscode >> 3u));
    /* All values in specification are K * 64,
       where   K = [2, 3, 6, 4, 5, 8, 7, 9, 10],
           i + 1 = [1, 2, 3, 4, 5, 6, 7, 8,  9],
       K - i - 1 = [1, 1, 3, 0, 0, 2, 0, 1,  2] = D.
       All values in D require only 2 bits to encode.
       Magic constant is shifted 6 bits left, to avoid final multiplication. */
    offset = (offset << 5u) + 0x40u + ((0x520D40u >> offset) & 0xC0u);
    return (uint16_t)(offset | bits64);
  }
}

static BROTLI_INLINE void GetLengthCode(size_t insertlen, size_t copylen,
                                        BROTLI_BOOL use_last_distance,
                                        uint16_t* code) {
  uint16_t inscode = GetInsertLengthCode(insertlen);
  uint16_t copycode = GetCopyLengthCode(copylen);
  *code = CombineLengthCodes(inscode, copycode, use_last_distance);
}

static BROTLI_INLINE uint32_t GetInsertBase(uint16_t inscode) {
  return kInsBase[inscode];
}

static BROTLI_INLINE uint32_t GetInsertExtra(uint16_t inscode) {
  return kInsExtra[inscode];
}

static BROTLI_INLINE uint32_t GetCopyBase(uint16_t copycode) {
  return kCopyBase[copycode];
}

static BROTLI_INLINE uint32_t GetCopyExtra(uint16_t copycode) {
  return kCopyExtra[copycode];
}

typedef struct Command {
  uint32_t insert_len_;
  /* Stores copy_len in low 25 bits and copy_code - copy_len in high 7 bit. */
  uint32_t copy_len_;
  /* Stores distance extra bits. */
  uint32_t dist_extra_;
  uint16_t cmd_prefix_;
  /* Stores distance code in low 10 bits
     and number of extra bits in high 6 bits. */
  uint16_t dist_prefix_;
} Command;

/* distance_code is e.g. 0 for same-as-last short code, or 16 for offset 1. */
static BROTLI_INLINE void InitCommand(Command* self,
    const BrotliDistanceParams* dist, size_t insertlen,
    size_t copylen, int copylen_code_delta, size_t distance_code) {
  /* Don't rely on signed int representation, use honest casts. */
  uint32_t delta = (uint8_t)((int8_t)copylen_code_delta);
  self->insert_len_ = (uint32_t)insertlen;
  self->copy_len_ = (uint32_t)(copylen | (delta << 25));
  /* The distance prefix and extra bits are stored in this Command as if
     npostfix and ndirect were 0, they are only recomputed later after the
     clustering if needed. */
  PrefixEncodeCopyDistance(
      distance_code, dist->num_direct_distance_codes,
      dist->distance_postfix_bits, &self->dist_prefix_, &self->dist_extra_);
  GetLengthCode(
      insertlen, (size_t)((int)copylen + copylen_code_delta),
      TO_BROTLI_BOOL((self->dist_prefix_ & 0x3FF) == 0), &self->cmd_prefix_);
}

static BROTLI_INLINE void InitInsertCommand(Command* self, size_t insertlen) {
  self->insert_len_ = (uint32_t)insertlen;
  self->copy_len_ = 4 << 25;
  self->dist_extra_ = 0;
  self->dist_prefix_ = BROTLI_NUM_DISTANCE_SHORT_CODES;
  GetLengthCode(insertlen, 4, BROTLI_FALSE, &self->cmd_prefix_);
}

static BROTLI_INLINE uint32_t CommandRestoreDistanceCode(
    const Command* self, const BrotliDistanceParams* dist) {
  if ((self->dist_prefix_ & 0x3FFu) <
      BROTLI_NUM_DISTANCE_SHORT_CODES + dist->num_direct_distance_codes) {
    return self->dist_prefix_ & 0x3FFu;
  } else {
    uint32_t dcode = self->dist_prefix_ & 0x3FFu;
    uint32_t nbits = self->dist_prefix_ >> 10;
    uint32_t extra = self->dist_extra_;
    uint32_t postfix_mask = (1U << dist->distance_postfix_bits) - 1U;
    uint32_t hcode = (dcode - dist->num_direct_distance_codes -
        BROTLI_NUM_DISTANCE_SHORT_CODES) >>
        dist->distance_postfix_bits;
    uint32_t lcode = (dcode - dist->num_direct_distance_codes -
        BROTLI_NUM_DISTANCE_SHORT_CODES) & postfix_mask;
    uint32_t offset = ((2U + (hcode & 1U)) << nbits) - 4U;
    return ((offset + extra) << dist->distance_postfix_bits) + lcode +
        dist->num_direct_distance_codes + BROTLI_NUM_DISTANCE_SHORT_CODES;
  }
}

static BROTLI_INLINE uint32_t CommandDistanceContext(const Command* self) {
  uint32_t r = self->cmd_prefix_ >> 6;
  uint32_t c = self->cmd_prefix_ & 7;
  if ((r == 0 || r == 2 || r == 4 || r == 7) && (c <= 2)) {
    return c;
  }
  return 3;
}

static BROTLI_INLINE uint32_t CommandCopyLen(const Command* self) {
  return self->copy_len_ & 0x1FFFFFF;
}

static BROTLI_INLINE uint32_t CommandCopyLenCode(const Command* self) {
  uint32_t modifier = self->copy_len_ >> 25;
  int32_t delta = (int8_t)((uint8_t)(modifier | ((modifier & 0x40) << 1)));
  return (uint32_t)((int32_t)(self->copy_len_ & 0x1FFFFFF) + delta);
}

#if defined(__cplusplus) || defined(c_plusplus)
}  /* extern "C" */
#endif

#endif  /* BROTLI_ENC_COMMAND_H_ */
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
