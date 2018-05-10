/*
** Copyright (C) 1999-2011 Erik de Castro Lopo <erikd@mega-nerd.com>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
*/

#include "sfconfig.h"

#include <stdio.h>
#include <stdlib.h>

#if HAVE_UNISTD_H
#include <unistd.h>
#else
#include "sf_unistd.h"
#endif

#include <sndfile.h>

#define	BUFFER_SIZE		(1024)
#define	CHNA_SIZE		(60000)
#define	AXML_SIZE		(60000)


static short buffer [BUFFER_SIZE] ;

int
main (int argc, char *argv [])
{
	SNDFILE	*file ;
	SF_INFO sfinfo ;
	int i, k, count, max = 0, total = 0 ;
	char *axml_data ;
	SF_CHNA_INFO chna_info ;


	if (argc < 2)
	{	printf ("Expecting input file name.\n") ;
		return 0 ;
		} ;

	if (! (file = sf_open (argv [1], SFM_READ, &sfinfo)))
	{	printf ("sf_open_read failed with error : ") ;
		puts (sf_strerror (NULL)) ;
		exit (1) ;
		} ;

    /* Read chna chunk */
	sf_command(file, SFC_GET_CHNA_INFO, (void *)&chna_info, sizeof(SF_CHNA_INFO)) ;
	printf("chna numTracks = %u\n", chna_info.numTracks) ;
	printf("chna numUIDs = %u\n", chna_info.numUIDs) ;
	for (k = 0; k < chna_info.numUIDs; k++)
	{
		printf("chna %d: %d\t", k, chna_info.audioID[k].trackIndex);
		for (i = 0; i < 12; i++)   printf("%c", chna_info.audioID[k].UID[i]) ;
		printf("\t");
		for (i = 0; i < 14; i++)   printf("%c", chna_info.audioID[k].trackRef[i]) ;
		printf("\t");
		for (i = 0; i < 11; i++)   printf("%c", chna_info.audioID[k].packRef[i]) ;
		printf("\n");
		} ;

 	/* Read axml chunk */
	axml_data = (char *)malloc(sizeof(char) * AXML_SIZE);
	sf_command(file, SFC_GET_AXML_INFO, (void *)axml_data, AXML_SIZE);
	printf("axml data:\n");
	printf("%s\n", axml_data);

	/* Read samples */
	while ((count = sf_read_short (file, buffer, BUFFER_SIZE)))
	{	for (k = 0 ; k < count ; k++)
			if (abs (buffer [k]) > max)
				max = abs (buffer [k]) ;
		total += count ;
		} ;

	printf ("Total samples : %d\n", total) ;
	printf ("Maximum value : %d\n", max) ;

	sf_close (file) ;

	free(axml_data);

	return 0 ;
} /* main */
