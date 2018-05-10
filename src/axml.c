/*
** Copyright (C) 2006-2016 Erik de Castro Lopo <erikd@mega-nerd.com>
** Copyright (C) 2006 Paul Davis <paul@linuxaudiosystems.com>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU Lesser General Public License as published by
** the Free Software Foundation; either version 2.1 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU Lesser General Public License for more details.
**
** You should have received a copy of the GNU Lesser General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
*/

#include "sfconfig.h"

#include <stdio.h>
#include <stddef.h>
#include <string.h>

#include "common.h"

#define SF_AXML_MAX_SIZE  0xFFFFFFFF

char*
axml_var_alloc (int len)
{
	return calloc (len, sizeof (char)) ;
} /* amxl_var_alloc */


int
axml_var_set (SF_PRIVATE *psf, const char * data, size_t datasize)
{	if (data == NULL)
		return SF_FALSE ;

	if (datasize >= SF_AXML_MAX_SIZE)
	{	psf->error = SFE_BAD_AXML_INFO_TOO_BIG ;
		return SF_FALSE ;
		} ;

	psf->axml_len = datasize ;

	/* Check for odd length data, and a add padding byte to make it even length */
	if ((psf->axml_len % 2) == 1)
	{	psf->axml_len += 1 ;
		} ;

	if (psf->axml_var == NULL)
	{	if ((psf->axml_var = axml_var_alloc (psf->axml_len)) == NULL)
		{	psf->error = SFE_MALLOC_FAILED ;
			return SF_FALSE ;
			} ;
		} ;

	memcpy (psf->axml_var, data, datasize) ;

	/* Add the padding char for the odd length data */
	if (datasize < psf->axml_len)
	{	psf->axml_var[datasize] = ' ' ;
		} ;

	return SF_TRUE ;
} /* axml_var_set */


int
axml_var_get (SF_PRIVATE *psf, char * data, size_t datasize)
{	size_t size ;

	if (psf->axml_var == NULL)
		return SF_FALSE ;

	size = datasize ;

	memcpy (data, psf->axml_var, size) ;

	return SF_TRUE ;
} /* axml_var_get */
