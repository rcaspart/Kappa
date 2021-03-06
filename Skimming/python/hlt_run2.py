import FWCore.ParameterSet.Config as cms
hltWhitelist = cms.vstring( ## HLT selection
	# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Trigger_Information
	# can be tested at https://regex101.com
	
	"^HLT_.*Mu[0-9]+.*_v[0-9]+$",
	"^HLT_.*Ele[0-9]+.*_v[0-9]+$",
	"^HLT_.*Tau[0-9]+.*_v[0-9]+$",
)

hltBlacklist = cms.vstring(
	"^HLT_.*Mu4[0-9]+.*_v[0-9]+$",
	"^HLT_.*Mu5[0-9]+.*_v[0-9]+$",
	"^HLT_.*Mu[0-9][0-9][0-9]+.*_v[0-9]+$",
	"^HLT_.*Ele[0-9][0-9][0-9]+.*_v[0-9]+$",
	"^HLT_.*Photon.*_v[0-9]+$",
	"^HLT_.*photon.*_v[0-9]+$",
	"^HLT_.*Jet.*_v[0-9]+$",
	"^HLT_.*jet.*_v[0-9]+$",
	"^HLT_.*MET.*_v[0-9]+$",
	"^HLT_.*Psi.*_v[0-9]+$",
	"^HLT_.*Mass.*_v[0-9]+$",
	"^HLT_.*HT[0-9]+.*_v[0-9]+$",
	"^HLT_(HI)?(L1|L2|L3)(L1|L2|L3)?(L1|L2|L3)?.*_v[0-9]+$",
	"^HLT_.*SameSign.*_v[0-9]+$",
	"^HLT_.*NoVertex.*_v[0-9]+$",
	"^HLT_.*NoVtx.*_v[0-9]+$",
	"^HLT_.*NoFilters.*_v[0-9]+$",
	"^HLT_.*SaveObjects.*_v[0-9]+$",
	"^HLT_.*_Di.*_v[0-9]+$",
	"^HLT_.*_Double.*_v[0-9]+$",
	"^HLT_.*_Bs.*_v[0-9]+$",
	"^HLT_.*_DZ.*_v[0-9]+$",
	"^HLT_.*Onia.*_v[0-9]+$",
	"^HLT_.*WHbbBoost.*_v[0-9]+$",
	"^HLT_.*dEta.*_v[0-9]+$",
	"^HLT_.*DiMu[0-9]+_Ele[0-9]+.*_v[0-9]+$",
)
