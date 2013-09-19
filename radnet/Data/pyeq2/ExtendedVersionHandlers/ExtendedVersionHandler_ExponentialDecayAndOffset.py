#    pyeq2 is a collection of equations expressed as Python classes
#
#    Copyright (C) 2012 James R. Phillips
#    2548 Vera Cruz Drive
#    Birmingham, AL 35235 USA
#
#    email: zunzun@zunzun.com
#    web: http://zunzun.com
#
#    License: BSD-style (see LICENSE.txt in main source directory)
#    Version info: $Id: ExtendedVersionHandler_ExponentialDecayAndOffset.py 5 2012-01-22 10:17:35Z zunzun.com@gmail.com $

import pyeq2
import IExtendedVersionHandler

import numpy
numpy.seterr(over = 'raise', divide = 'raise', invalid = 'raise', under = 'ignore') # numpy raises warnings, convert to exceptions to trap them


class ExtendedVersionHandler_ExponentialDecayAndOffset(IExtendedVersionHandler.IExtendedVersionHandler):
    
    def AssembleDisplayHTML(self, inModel):
        x_or_xy = 'xy'
        if inModel.GetDimensionality() == 2:
            x_or_xy = 'x'
            
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return inModel._HTML + '<br>' + inModel._leftSideHTML + ' = ' + inModel._leftSideHTML + ' / exp(' + x_or_xy + ') + Offset'
        else:
            try:
                cd = inModel.GetCoefficientDesignators()
                return inModel._HTML + '<br>' + inModel._leftSideHTML + ' = ' + inModel._leftSideHTML + ' / (' + inModel.listOfAdditionalCoefficientDesignators[len(cd)] + ' * exp(' + x_or_xy + ')) + Offset'
            except:
                return inModel._HTML + '<br>' + inModel._leftSideHTML + ' = ' + inModel._leftSideHTML + ' / (exp(' + x_or_xy + ')) + Offset'


    def AssembleDisplayName(self, inModel):
        return inModel._baseName + ' With Exponential Decay And Offset'


    def AssembleSourceCodeName(self, inModel):
        return inModel.__class__.__name__ + "_ExponentialDecayAndOffset"


    def AssembleCoefficientDesignators(self, inModel):
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return inModel._coefficientDesignators + ['Offset']
        else:
            return inModel._coefficientDesignators + [inModel.listOfAdditionalCoefficientDesignators[len(inModel._coefficientDesignators)], 'Offset']


    def AssembleOutputSourceCodeCPP(self, inModel):
        x_or_xy = 'x_in * y_in'
        if inModel.GetDimensionality() == 2:
            x_or_xy = 'x_in'
            
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return inModel.SpecificCodeCPP() + "temp = temp / exp(" + x_or_xy + ") + Offset;\n"
        else:
            cd = inModel.GetCoefficientDesignators()
            return inModel.SpecificCodeCPP() + "temp = temp / ("  + cd[len(cd)-2] + ' * exp(' + x_or_xy + ")) + Offset;\n"
        

    def GetAdditionalDataCacheFunctions(self, inModel, inDataCacheFunctions):
        foundX = False
        foundXY = False
        for i in inDataCacheFunctions: # if these are already in the cache, we don't need to add them again
            if i[0] == 'ExpX' and inModel.GetDimensionality() == 2:
                foundX = True
            if i[0] == 'ExpXY' and inModel.GetDimensionality() == 3:
                foundXY = True
                
        if inModel.GetDimensionality() == 2:
            if not foundX:
                return inDataCacheFunctions + \
                       [[pyeq2.DataCache.DataCacheFunctions.ExpX(NameOrValueFlag=1), []]]
        else:
            if not foundXY:
                return inDataCacheFunctions + \
                       [[pyeq2.DataCache.DataCacheFunctions.ExpXY(NameOrValueFlag=1), []]]
        return inDataCacheFunctions


    def GetAdditionalModelPredictions(self, inBaseModelCalculation, inCoeffs, inDataCacheDictionary, inModel):
        if inModel.GetDimensionality() == 2:
            if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
                return inBaseModelCalculation / inDataCacheDictionary['ExpX'] + inCoeffs[len(inCoeffs)-1]
            else:
                return inBaseModelCalculation / (inCoeffs[len(inCoeffs)-2] * inDataCacheDictionary['ExpX']) + inCoeffs[len(inCoeffs)-1]
        else:
            if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
                return inBaseModelCalculation / inDataCacheDictionary['ExpXY'] + inCoeffs[len(inCoeffs)-1]
            else:
                return inBaseModelCalculation / (inCoeffs[len(inCoeffs)-2] * inDataCacheDictionary['ExpXY']) + inCoeffs[len(inCoeffs)-1]