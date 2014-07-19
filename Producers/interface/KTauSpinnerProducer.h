/* Copyright (c) 2010 - All Rights Reserved
 *   Armin Burgmeier <burgmeier@ekp.uni-karlsruhe.de>
 *   Fred Stober <stober@cern.ch>
 *   Manuel Zeise <zeise@cern.ch>
 */

#ifndef KAPPA_TAUSPINNERPRODUCER_H
#define KAPPA_TAUSPINNERPRODUCER_H

#include "KBaseMultiProducer.h"

class KTauSpinnerProducer : public KBaseMultiProducer<bool, KTauSpinner>
{
public:
	KTauSpinnerProducer(const edm::ParameterSet &cfg, TTree *_event_tree, TTree *_lumi_tree) :
		KBaseMultiProducer<bool, KTauSpinner>(cfg, _event_tree, _lumi_tree, getLabel()) {}

	static const std::string getLabel() { return "TauSpinner"; }

protected:
	virtual void fillProduct(const InputType &in, OutputType &out,
		const std::string &name, const edm::InputTag *tag, const edm::ParameterSet &pset)
	{
		edm::Handle<bool> TauSpinnerHandle;
		this->cEvent->getByLabel(*tag, TauSpinnerHandle);

		out.WTisValid = *TauSpinnerHandle;
		//std::cout << "normaler tag: " <<tag->encode() << std::endl;
		edm::Handle<double> TauSpinnerHandleWT;
		edm::InputTag tsTagWT("TauSpinnerReco:TauSpinnerWT:KAPPA");
		//std::cout << "custom tag: " <<tsTagWT.encode() << std::endl;
		this->cEvent->getByLabel(tsTagWT, TauSpinnerHandleWT);
		out.WT = *TauSpinnerHandleWT;

		edm::Handle<double> TauSpinnerHandleWTFlip;
		edm::InputTag tsTagWTHFlip("TauSpinnerReco:TauSpinnerWTFlip:KAPPA");
		this->cEvent->getByLabel(tsTagWTHFlip, TauSpinnerHandleWTFlip);
		out.WTFlip = *TauSpinnerHandleWTFlip;

		edm::Handle<double> TauSpinnerHandleWThminus;
		edm::InputTag tsTagWThminus("TauSpinnerReco:TauSpinnerWThminus:KAPPA");
		this->cEvent->getByLabel(tsTagWThminus, TauSpinnerHandleWThminus);
		out.WThminus = *TauSpinnerHandleWThminus;

		edm::Handle<double> TauSpinnerHandleWThplus;
		edm::InputTag tsTagWThplus("TauSpinnerReco:TauSpinnerWThplus:KAPPA");
		this->cEvent->getByLabel(tsTagWThplus, TauSpinnerHandleWThplus);
		out.WThplus = *TauSpinnerHandleWThplus;

	}
	virtual void clearProduct(OutputType &output) { }
};

#endif
