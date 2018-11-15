<<<<<<< HEAD
/*
 * fcache.c
 *
 * SOFTWARE RIGHTS
 *
 * We reserve no LEGAL rights to the Purdue Compiler Construction Tool
 * Set (PCCTS) -- PCCTS is in the public domain.  An individual or
 * company may do whatever they wish with source code distributed with
 * PCCTS or the code generated by PCCTS, including the incorporation of
 * PCCTS, or its output, into commerical software.
 *
 * We encourage users to develop software with PCCTS.  However, we do ask
 * that credit is given to us for developing PCCTS.  By "credit",
 * we mean that if you incorporate our source code into one of your
 * programs (commercial product, research project, or otherwise) that you
 * acknowledge this fact somewhere in the documentation, research report,
 * etc...  If you like PCCTS and have developed a nice tool with the
 * output, please mention that you developed it using PCCTS.  In
 * addition, we ask that this header remain intact in our source code.
 * As long as these guidelines are kept, we expect to continue enhancing
 * this system and expect to make other tools available as they are
 * completed.
 *
 * ANTLR 1.33MR10
 *
 */

#include <stdio.h>
#include <ctype.h>

#include "pcctscfg.h"

#include "set.h"
#include "syn.h"
#include "hash.h"
#include "generic.h"

#ifdef __USE_PROTOS
CacheEntry *dumpFcache1(char *prev)
#else
CacheEntry *dumpFcache1(prev)
  char  *prev;
#endif
{
    Entry   **table=Fcache;

    int     low=0;
    int     hi=0;

    CacheEntry  *least=NULL;

	Entry   **p;

	for (p=table; p<&(table[HashTableSize]); p++) {

		CacheEntry *q =(CacheEntry *) *p;
		
		if ( q != NULL && low==0 ) low = p-table;
		while ( q != NULL ) {
            if (strcmp(q->str,prev) > 0) {
              if (least == NULL) {
                least=q;
              } else {
                if (strcmp(q->str,least->str) < 0) {
                  least=q;
                };
              };
            };
			q = q->next;
		};

		if ( *p != NULL ) hi = p-table;
	}
    return least;
}

#ifdef __USE_PROTOS
void reportFcache(CacheEntry *q)
#else
void reportFcache(q)
  CacheEntry    *q;
#endif
{
    char        *qstr;

    fprintf(stdout,"\nrule ");
    for (qstr=q->str; *qstr != '*' ; qstr++) {
      fprintf(stdout,"%c",*qstr);
    };

    qstr++;
    if (*qstr == 'i') fprintf(stdout," First[");
    if (*qstr == 'o') fprintf(stdout," Follow[");
    qstr++;
    fprintf(stdout,"%s]",qstr);
    if (q->incomplete) fprintf(stdout," *** incomplete ***");
    fprintf(stdout,"\n");
    MR_dumpTokenSet(stdout,1,q->fset);
}

void 
#ifdef __USE_PROTOS
DumpFcache(void) 
#else
DumpFcache() 
#endif
{

    char        *prev="";
    int          n=0;
    CacheEntry  *next;

    fprintf(stdout,"\n\nDump of First/Follow Cache\n");

    for(;;) {
      next=dumpFcache1(prev);
      if (next == NULL) break;
      reportFcache(next);
      ++n;
      prev=next->str;
    };
    fprintf(stdout,"\nEnd dump of First/Follow Cache\n");
}
=======
/*
 * fcache.c
 *
 * SOFTWARE RIGHTS
 *
 * We reserve no LEGAL rights to the Purdue Compiler Construction Tool
 * Set (PCCTS) -- PCCTS is in the public domain.  An individual or
 * company may do whatever they wish with source code distributed with
 * PCCTS or the code generated by PCCTS, including the incorporation of
 * PCCTS, or its output, into commerical software.
 *
 * We encourage users to develop software with PCCTS.  However, we do ask
 * that credit is given to us for developing PCCTS.  By "credit",
 * we mean that if you incorporate our source code into one of your
 * programs (commercial product, research project, or otherwise) that you
 * acknowledge this fact somewhere in the documentation, research report,
 * etc...  If you like PCCTS and have developed a nice tool with the
 * output, please mention that you developed it using PCCTS.  In
 * addition, we ask that this header remain intact in our source code.
 * As long as these guidelines are kept, we expect to continue enhancing
 * this system and expect to make other tools available as they are
 * completed.
 *
 * ANTLR 1.33MR10
 *
 */

#include <stdio.h>
#include <ctype.h>

#include "pcctscfg.h"

#include "set.h"
#include "syn.h"
#include "hash.h"
#include "generic.h"

#ifdef __USE_PROTOS
CacheEntry *dumpFcache1(char *prev)
#else
CacheEntry *dumpFcache1(prev)
  char  *prev;
#endif
{
    Entry   **table=Fcache;

    int     low=0;
    int     hi=0;

    CacheEntry  *least=NULL;

	Entry   **p;

	for (p=table; p<&(table[HashTableSize]); p++) {

		CacheEntry *q =(CacheEntry *) *p;
		
		if ( q != NULL && low==0 ) low = p-table;
		while ( q != NULL ) {
            if (strcmp(q->str,prev) > 0) {
              if (least == NULL) {
                least=q;
              } else {
                if (strcmp(q->str,least->str) < 0) {
                  least=q;
                };
              };
            };
			q = q->next;
		};

		if ( *p != NULL ) hi = p-table;
	}
    return least;
}

#ifdef __USE_PROTOS
void reportFcache(CacheEntry *q)
#else
void reportFcache(q)
  CacheEntry    *q;
#endif
{
    char        *qstr;

    fprintf(stdout,"\nrule ");
    for (qstr=q->str; *qstr != '*' ; qstr++) {
      fprintf(stdout,"%c",*qstr);
    };

    qstr++;
    if (*qstr == 'i') fprintf(stdout," First[");
    if (*qstr == 'o') fprintf(stdout," Follow[");
    qstr++;
    fprintf(stdout,"%s]",qstr);
    if (q->incomplete) fprintf(stdout," *** incomplete ***");
    fprintf(stdout,"\n");
    MR_dumpTokenSet(stdout,1,q->fset);
}

void 
#ifdef __USE_PROTOS
DumpFcache(void) 
#else
DumpFcache() 
#endif
{

    char        *prev="";
    int          n=0;
    CacheEntry  *next;

    fprintf(stdout,"\n\nDump of First/Follow Cache\n");

    for(;;) {
      next=dumpFcache1(prev);
      if (next == NULL) break;
      reportFcache(next);
      ++n;
      prev=next->str;
    };
    fprintf(stdout,"\nEnd dump of First/Follow Cache\n");
}
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
