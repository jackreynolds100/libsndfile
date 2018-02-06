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

/* i'm not sure if chna.c is neceesary for BW64*/

SF_CHNA_INFO_16K*
chna_var_alloc (void)
{
	return calloc (1, sizeof (SF_CHNA_INFO_16K)) ;
} /* chna_var_alloc */

int
chna_var_set (SF_PRIVATE *psf, const SF_CHNA_INFO * info, size_t datasize)
{	size_t len ;

	if (info == NULL)
		return SF_FALSE ;

	if (datasize >= sizeof (SF_CHNA_INFO_16K))
	{	psf->error = SFE_BAD_CHNA_INFO_TOO_BIG ;
		return SF_FALSE ;
		} ;

	if (psf->chna_16k == NULL)
	{	if ((psf->chna_16k = chna_var_alloc ()) == NULL)
		{	psf->error = SFE_MALLOC_FAILED ;
			return SF_FALSE ;
			} ;
		} ;

	return SF_TRUE ;
} /* chna_var_set */


int
chna_var_get (SF_PRIVATE *psf, SF_CHNA_INFO * data, size_t datasize)
{	size_t size ;

  printf("chna_var_get: %d", datasize);
	if (psf->chna_16k == NULL)
		return SF_FALSE ;

	size = datasize ;

	memcpy (data, psf->chna_16k, size) ;

	return SF_TRUE ;
} /* chna_var_get */
