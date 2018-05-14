/*
** Copyright (C) 1999-2012 Erik de Castro Lopo <erikd@mega-nerd.com>
**
** All rights reserved.
**
** Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**
**     * Redistributions of source code must retain the above copyright
**       notice, this list of conditions and the following disclaimer.
**     * Redistributions in binary form must reproduce the above copyright
**       notice, this list of conditions and the following disclaimer in
**       the documentation and/or other materials provided with the
**       distribution.
**     * Neither the author nor the names of any contributors may be used
**       to endorse or promote products derived from this software without
**       specific prior written permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
** TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
** PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
** CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
** EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
** PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
** OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
** WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
** OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
** ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include	<stdio.h>
#include	<stdlib.h>
#include	<string.h>
#include	<math.h>

#include	<sndfile.h>

#ifndef		M_PI
#define		M_PI		3.14159265358979323846264338
#endif

#define		SAMPLE_RATE			48000
#define		SAMPLE_COUNT		(SAMPLE_RATE * 1)  /* A second of audio. Change 1 to 15000 if you want a >4gb file. */
#define		AMPLITUDE			(1.0 * 0x7F000000)
#define		LEFT_FREQ			(344.0 / SAMPLE_RATE)
#define		RIGHT_FREQ			(466.0 / SAMPLE_RATE)


int		GenerateAxml(char **axml_info) ;
void	GenerateChna(SF_CHNA_INFO *chna_info, int num_ch) ;
void	ByteFill(char *var, char *str, int val, int len);


int
main (void)
{	SNDFILE	*file ;
	SF_INFO	sfinfo ;
	int k ;
	int	*buffer ;
	SF_CHNA_INFO chna_info;
	char *axml_info;
	int axml_len;


	if (! (buffer = malloc (2 * SAMPLE_COUNT * sizeof (int))))
	{	printf ("Error : Malloc failed.\n") ;
		return 1 ;
		} ;


	memset (&sfinfo, 0, sizeof (sfinfo)) ;

	sfinfo.samplerate	= SAMPLE_RATE ;
	sfinfo.frames		= SAMPLE_COUNT ;
	sfinfo.channels		= 2 ;
	sfinfo.format		= (SF_FORMAT_BW64 | SF_FORMAT_PCM_24) ;

	if (! (file = sf_open ("BW64_sine.wav", SFM_WRITE, &sfinfo)))
	{
		printf ("Error : Not able to open output file.\n") ;
		free (buffer) ;
		return 1 ;
		} ;

	/* Enable auto downgrade on file close. */

	sf_command(file, SFC_BW64_AUTO_DOWNGRADE, NULL, SF_TRUE) ;

	GenerateChna(&chna_info, sfinfo.channels) ;

	axml_len = GenerateAxml(&axml_info) ;

	printf("axml_info: %s\n", axml_info) ;
	printf("axml_info size: %d\n", axml_len) ;

	sf_command(file, SFC_SET_CHNA_INFO, (void *)&chna_info, sizeof(chna_info)) ;
	sf_command(file, SFC_SET_AXML_INFO, (void *)axml_info, axml_len) ;

	if (sfinfo.channels == 1)
	{	for (k = 0 ; k < SAMPLE_COUNT ; k++)
		{	buffer [k] = AMPLITUDE * sin (LEFT_FREQ * 2 * k * M_PI) ;
			} ;
		}
	else if (sfinfo.channels == 2)
	{	for (k = 0 ; k < SAMPLE_COUNT ; k++)
		{	buffer [2 * k] = AMPLITUDE * sin (LEFT_FREQ * 2 * k * M_PI) ;
			buffer [2 * k + 1] = AMPLITUDE * sin (RIGHT_FREQ * 2 * k * M_PI) ;
			} ;
		}
	else
	{	printf ("Error : make_sine can only generate mono or stereo files.\n") ;
		sf_close (file) ;
		free (buffer) ;
		return 1 ;
		} ;

	if (sf_write_int (file, buffer, sfinfo.channels * SAMPLE_COUNT) != sfinfo.channels * SAMPLE_COUNT)
		puts (sf_strerror (file)) ;

	sf_close (file) ;
	free (buffer) ;
	return 0 ;
} /* main */


int
GenerateAxml(char **axml_info)
{
	char str[4096] ;

    /* Some ADM XML to represent stereo channels */
	sprintf(str, "\
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n \
<ebuCoreMain xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns=\"urn:ebu:metadata-schema:ebuCore\" xml:lang=\"en\">\n\
    <format>\n\
      <audioFormatExtended>\n\
        <audioProgramme audioProgrammeID=\"APR_1001\" audioProgrammeName=\"Test\">\n\
          <audioContentIDRef>ACO_1001/audioContentIDRef>\n\
        </audioProgramme>\n\
        <audioContent audioContentID=\"ACO_1001\" audioContentName=\"Test\">\n\
          <audioObjectIDRef>AO_1001</audioObjectIDRef>\n\
        </audioContent>\n\
        <audioObject audioObjectID=\"AO_1001\" audioObjectName=\"Main\">\n\
          <audioPackFormatIDRef>AP_00010002</audioPackFormatIDRef>\n\
          <audioTrackUIDRef>ATU_00000001</audioTrackUIDRef>\n\
          <audioTrackUIDRef>ATU_00000002</audioTrackUIDRef>\n\
        </audioObject>\n\
        <audioTrackUID UID=\"ATU_00000001\" sampleRate=\"48000\" bitDepth=\"24\"/>\n\
        <audioTrackUID UID=\"ATU_00000002\" sampleRate=\"48000\" bitDepth=\"24\"/>\n\
      </audioFormatExtended>\n\
    </format>\n\
  </coreMetadata>\n\
</ebuCoreMain>\n") ;

	*axml_info = (char *)malloc(strlen(str) * sizeof(char)) ;
	memcpy(*axml_info, str, strlen(str) * sizeof(char)) ;

	return strlen(str) ;
}


void
GenerateChna(SF_CHNA_INFO *chna_info, int num_ch)
{
	int k ;
	chna_info->numTracks = num_ch ;
	chna_info->numUIDs = num_ch ;
	for (k = 0; k < chna_info->numUIDs; k++)
	{	chna_info->audioID[k].trackIndex = k + 1 ;
		ByteFill(chna_info->audioID[k].UID, "ATU_%08x", k + 1, 12) ;
		ByteFill(chna_info->audioID[k].trackRef, "AT_00010%03x_01", k + 1, 14) ;
		ByteFill(chna_info->audioID[k].packRef, "AP_00010002", 0, 11) ;
		chna_info->audioID[k].pad = '\0' ;
		} ;
}


void
ByteFill(char *var, char *str, int val, int len)
{
	int i;
	char ch2[20];
	for (i = 0; i < 20; i++)
		ch2[i] = '\0';

	sprintf(ch2, str, val);
	for (i = 0; i < len; i++)
		var[i] = ch2[i];
}
