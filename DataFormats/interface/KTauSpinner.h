/* Copyright (c) 2010 - All Rights Reserved
 *   Armin Burgmeier <burgmeier@ekp.uni-karlsruhe.de>
 *   Fred Stober <stober@cern.ch>
 *   Manuel Zeise <zeise@cern.ch>
 */

#ifndef KAPPA_TAUSPINNER_H
#define KAPPA_TAUSPINNER_H

struct KTauSpinner
{
	bool WTisValid;
	double WT;
	double WTFlip;
	double WThminus;
	double WThplus;
};

#endif
