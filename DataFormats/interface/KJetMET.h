/* Copyright (c) 2010 - All Rights Reserved
 *   Armin Burgmeier <burgmeier@ekp.uni-karlsruhe.de>
 *   Fred Stober <stober@cern.ch>
 *   Joram Berger <joram.berger@cern.ch>
 *   Manuel Zeise <zeise@cern.ch>
 *   Thomas Hauth <Thomas.Hauth@cern.ch>
 */

#ifndef KAPPA_JET_H
#define KAPPA_JET_H

#include <Math/SMatrix.h>
#include "KBasic.h"
#include "KInfo.h"

struct KCaloJet : public KLV
{
	double area;
	double fHPD, fRBX;
	double fEM, fHO;
	int nConst, n90Hits;
};
typedef std::vector<KCaloJet> KCaloJets;

struct KBasicJet : public KLV
{
	double area;
	float neutralEMFraction, chargedEMFraction;
	float neutralHadFraction, chargedHadFraction;
	float muonFraction, photonFraction, electronFraction;
	float HFHadFraction, HFEMFraction;

	int nConst, nCharged;
};
typedef std::vector<KBasicJet> KBasicJets;

struct KJet : public KBasicJet
{
    std::vector<float> taggers;
    unsigned int puJetID;

    float getTagger(const std::string &name, const KJetMetadata *taggermetadata) const
    {
 		for (unsigned int i = 0; i < taggermetadata->taggernames.size(); ++i)
        {
            if (taggermetadata->taggernames[i] == name)
				return taggers[i];
		}
		std::cout << "Tagger " << name << " not available!" << std::endl;
		exit(1);
    }

    bool getpuJetID(const std::string &name, const KJetMetadata *taggermetadata) const
    {
		for (unsigned int i = 0; i < taggermetadata->pujetidnames.size(); ++i)
        {
            if (taggermetadata->pujetidnames[i] == name)
                return puJetID & (1 << i);
        }
		std::cout << "PUJetID " << name << " not available!" << std::endl;
		exit(1);
    }

};

typedef std::vector<KJet> KJets;

struct KBasicMET : public KLV
{
	double sumEt;

	ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > significance;
};

struct KMET : public KBasicMET
{
	double chargedEMEtFraction, chargedHadEtFraction;
	double neutralEMEtFraction, neutralHadEtFraction;
	double muonEtFraction;
	double type6EtFraction, type7EtFraction;
};

struct KHCALNoiseSummary
{
	bool hasBadRBXTS4TS5;
	float isolatedNoiseSumE;
	float isolatedNoiseSumEt;
	float max25GeVHitTime;
	float maxE2Over10TS;
	int maxHPDHits;
	int maxHPDNoOtherHits;
	int maxRBXHits;
	int maxZeros;
	float min25GeVHitTime;
	float minE2Over10TS;
	float minRBXEMF;
	int numIsolatedNoiseChannels;
};

struct KPileupDensity
{
	double rho;
	double sigma;
};

#endif
