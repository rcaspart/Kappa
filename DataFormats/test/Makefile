PROGRAM  = libKappa.so libKappa.a libKappa.o

CXX      = g++
CXXFLAGS = -O2 -Wall -fPIC -std=c++11 $(shell root-config --cflags | sed 's/-I/-isystem /') -I../../../
WARNINGS = -Wextra -Wno-unused-parameter -Wswitch-enum -Wsync-nand \
           -Wtrampolines -Wfloat-equal -Wpacked -Wwrite-strings \
           -Wstrict-overflow=3 -Wredundant-decls -Wdisabled-optimization -Wdouble-promotion \
           -Wnormalized=nfkc -Wlogical-op -Wstack-protector -Wmissing-include-dirs \
           -Wmissing-format-attribute -Wundef -Wshadow -Wcast-align \
           -Wunreachable-code
# additional warnings that show up in dictionary code created by ROOT
#          -Wconversion -Wuseless-cast -Wcast-equal -Wswitch-default -Wmissing-declarations
LDFLAGS  = -O $(shell root-config --libs) $(SYSLIBS) -L$(ROOFITSYS)lib\
	-lGenVector -lMathCore -lRooFitCore

# Boost
# Use Boost from CMSSW if CMSSW env available otherwise fall back to system boost
BOOST_INCDIR = $(shell test ! -z $(CMSSW_BASE) && cd $(CMSSW_BASE) && scram tool info boost | sed -n 's/INCLUDE=/-isystem/p')
CXXFLAGS += $(BOOST_INCDIR) -I$(ROOFITSYS)include

all: $(PROGRAM)

CrystalBallEfficiency.o: ../src/CrystalBallEfficiency.cpp
	@echo $(CXX) $(CXXFLAGS) -c -o $@ $<
	@$(CXX) $(CXXFLAGS) $(WARNINGS) -c -o $@ $<

Hash.o: ../src/Hash.cpp
	@echo $(CXX) $(CXXFLAGS) -c -o $@ $<
	@$(CXX) $(CXXFLAGS) $(WARNINGS) -c -o $@ $<

%.o: %.cpp
	@echo $(CXX) $(CXXFLAGS) -c -o $@ $<
	@$(CXX) $(CXXFLAGS) $(WARNINGS) -c -o $@ $<

%.a: %.o KDebug.o
	ar rcs $@ $^
	mkdir -p ../../lib
	cp $@ ../../lib

%.so: %.o KDebug.o Hash.o CrystalBallEfficiency.o
	$(CXX) $(LDFLAGS) -shared -o $@ $^
	mkdir -p ../../lib
	cp $@ ../../lib

%.sbin: %.o libKappa.o
	$(CXX) $(LDFLAGS) -o $@ $^

libKappa.cpp: standalone.h ../src/classes.h LinkDef.h
	rootcint -f $@ -c -I$(ROOFITSYS)include $^

install: $(PROGRAM)

clean:
	@rm -f *.o libKappa.* ../../lib/*
