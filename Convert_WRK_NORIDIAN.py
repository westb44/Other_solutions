import xlrd
import sys
import string
import time
import math
import unicodedata

print "    Start of: ", sys.argv[0]

book = xlrd.open_workbook(sys.argv[1])

outputFile = ''.join(sys.argv[1])
#replace blanks with underscore in output file name
outputFile = outputFile.replace(" ", "_")
#replace .xls with .txt in output file name
outputFile = outputFile.replace(".xls", ".txt")

print "  Input file: ", sys.argv[1]
print " Output file: ", outputFile

sh = book.sheet_by_index(0)

f = open(outputFile, 'w')
strRecord = " "
tempfield = " "
vbtab = "\t"
for rx in range(sh.nrows):
    if rx > 0:
       if 'Inactive' in sys.argv[1]:
            strRecord = str(sh.cell(rx,0).value) + vbtab               # NDC
            y= str(sh.cell(rx,1).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # NDC_MOD
            else:
                strRecord = strRecord + str(sh.cell(rx,1).value) + vbtab   # NDC_MOD
            strRecord = strRecord + str(sh.cell(rx,2).value) + vbtab   # HCPCS
            y= str(sh.cell(rx,1).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # HCPCS_MOD
            else:
                strRecord = strRecord + str(sh.cell(rx,3).value) + vbtab   # HCPCS_MOD
            #--- release end date
            x= str(sh.cell(rx,4).value)
            z=(x.split(".")[0])
            z1 = int(z)
            if z1 < 61:
               z1 = 61
            y = xlrd.xldate_as_tuple(z1,0)
            strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # REL_START_DATE conversion           
            #tempfield = str(sh.cell(rx,5).value) #+ vbtab
            #--- release end date
            #if tempfield != '99/99/9999':
            #   x= str(sh.cell(rx,5).value)
            #   z=(x.split(".")[0])
            #   z1 = int(z)
            #   if z1 < 61:
            #      z1 = 61
            #   y = xlrd.xldate_as_tuple(z1,0)
            #   strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # REL_END_DATE conversion
            #else:
            strRecord = strRecord + str(sh.cell(rx,5).value) + vbtab   # REL_END_DATE
            tempfield = unicode(sh.cell(rx,6).value) + vbtab
            tempfield = unicodedata.normalize('NFKD',tempfield).encode('ascii', 'ignore')
            strRecord = strRecord + tempfield  # HCPCS_DESC
            strRecord = strRecord + str(sh.cell(rx,7).value) + vbtab  # NDC_LABEL
            strRecord = strRecord + str(sh.cell(rx,8).value) + vbtab   # NDC_PKG
            strRecord = strRecord + str(sh.cell(rx,9).value) + vbtab   # NDC_PKG_MEA
            y= str(sh.cell(rx,10).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # NDC_PKG_TYPE
            else:
                strRecord = strRecord + str(sh.cell(rx,10).value) + vbtab   # NDC_PKG_TYPE
            strRecord = strRecord + str(sh.cell(rx,11).value) + vbtab  # ROUT_OF_ADMIN
            strRecord = strRecord + str(sh.cell(rx,12).value) + vbtab  # BILLING_UNITS
            strRecord = strRecord + str(sh.cell(rx,13).value) + vbtab  # HCPCS_AMT1
            strRecord = strRecord + str(sh.cell(rx,14).value) + vbtab  # HCPCS_MEASURE1
            strRecord = strRecord + str(sh.cell(rx,15).value) + vbtab  # CF
            strRecord = strRecord + str(sh.cell(rx,16).value) + vbtab  # START_DATE1
            strRecord = strRecord + str(sh.cell(rx,17).value) + vbtab  # END_DATE_1
            y= str(sh.cell(rx,18).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_START_DATE_2
            else:
                strRecord = strRecord + str(sh.cell(rx,18).value) + vbtab  # PRIOR_START_DATE_2
            y= str(sh.cell(rx,19).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_END_DATE_2
            else:
                strRecord = strRecord + str(sh.cell(rx,19).value) + vbtab  # PRIOR_END_DATE_2
            y= str(sh.cell(rx,20).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_CONVERSION_FACTOR_2
            else:
                strRecord = strRecord + str(sh.cell(rx,20).value) + vbtab  # PRIOR_CONVERSION_FACTOR_2
            y= str(sh.cell(rx,21).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_START_DATE_3
            else:
                strRecord = strRecord + str(sh.cell(rx,21).value) + vbtab  # PRIOR_START_DATE_3
            y= str(sh.cell(rx,22).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_END_DATE_3
            else:
                strRecord = strRecord + str(sh.cell(rx,22).value) + vbtab  # PRIOR_END_DATE_3
            y= str(sh.cell(rx,23).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_CONVERSION_FACTOR_3
            else:
                strRecord = strRecord + str(sh.cell(rx,23).value) + vbtab  # PRIOR_CONVERSION_FACTOR_3
            #--- start date 1
            #x= str(sh.cell(rx,16).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # START_DATE1 conversion
            #--- end date 1
            #x= str(sh.cell(rx,17).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #   y = xlrd.xldate_as_tuple(z1,0)
            #   strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PR_OHP_ELIG_DT conversion
            #--- priority start date 2
            #x= str(sh.cell(rx,18).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # # PRI_START_DATE2 conversion
            #--- priority end date2
            #x= str(sh.cell(rx,19).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #   z1 = 61
            #   y = xlrd.xldate_as_tuple(z1,0)
            #   strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PRI_END_DATE2 conversion
            #strRecord = strRecord + str(sh.cell(rx,20).value) + vbtab  # PRI_CONV_FACT2
            #--- priority start date 3
            #x= str(sh.cell(rx,21).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PRI_START_DATE3 conversion
            #--- pririty end date 3
            #x= str(sh.cell(rx,22).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PRI_END_DATE3 conversion
            #strRecord = strRecord + str(sh.cell(rx,23).value) + vbtab  # PRI_CONV_FACT3

       else:
            strRecord = str(sh.cell(rx,0).value) + vbtab               # NDC
            y= str(sh.cell(rx,1).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # NDC_MOD
            else:
                strRecord = strRecord + str(sh.cell(rx,1).value) + vbtab   # NDC_MOD
            strRecord = strRecord + str(sh.cell(rx,2).value) + vbtab   # HCPCS
            y= str(sh.cell(rx,1).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # HCPCS_MOD
            else:
                strRecord = strRecord + str(sh.cell(rx,3).value) + vbtab   # HCPCS_MOD
            #--- release end date
            x= str(sh.cell(rx,4).value)
            z=(x.split(".")[0])
            z1 = int(z)
            if z1 < 61:
               z1 = 61
            y = xlrd.xldate_as_tuple(z1,0)
            strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # REL_START_DATE conversion           
            #tempfield = str(sh.cell(rx,5).value) #+ vbtab
            #--- release end date
            #if tempfield != '99/99/9999':
            #   x= str(sh.cell(rx,5).value)
            #   z=(x.split(".")[0])
            #   z1 = int(z)
            #   if z1 < 61:
            #      z1 = 61
            #   y = xlrd.xldate_as_tuple(z1,0)
            #   strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # REL_END_DATE conversion
            #else:
            strRecord = strRecord + str(sh.cell(rx,5).value) + vbtab   # REL_END_DATE
            tempfield = unicode(sh.cell(rx,6).value) + vbtab
            tempfield = unicodedata.normalize('NFKD',tempfield).encode('ascii', 'ignore')
            strRecord = strRecord + tempfield  # HCPCS_DESC
            strRecord = strRecord + str(sh.cell(rx,7).value) + vbtab  # NDC_LABEL
            strRecord = strRecord + str(sh.cell(rx,8).value) + vbtab   # NDC_PKG
            strRecord = strRecord + str(sh.cell(rx,9).value) + vbtab   # NDC_PKG_MEA
            y= str(sh.cell(rx,10).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # NDC_PKG_TYPE
            else:
                strRecord = strRecord + str(sh.cell(rx,10).value) + vbtab   # NDC_PKG_TYPE
            strRecord = strRecord + str(sh.cell(rx,11).value) + vbtab  # ROUT_OF_ADMIN
            strRecord = strRecord + str(sh.cell(rx,12).value) + vbtab  # BILLING_UNITS
            strRecord = strRecord + str(sh.cell(rx,13).value) + vbtab  # HCPCS_AMT1
            strRecord = strRecord + str(sh.cell(rx,14).value) + vbtab  # HCPCS_MEASURE1
            strRecord = strRecord + str(sh.cell(rx,15).value) + vbtab  # CF
            x= str(sh.cell(rx,16).value)
            z=(x.split(".")[0])
            z1 = int(z)
            if z1 < 61:
               z1 = 61
            y = xlrd.xldate_as_tuple(z1,0)
            strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # REL_START_DATE conversion 
            #strRecord = strRecord + str(sh.cell(rx,16).value) + vbtab  # START_DATE1
            strRecord = strRecord + str(sh.cell(rx,17).value) + vbtab  # END_DATE_1
            y= str(sh.cell(rx,18).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_START_DATE_2
            else:
                strRecord = strRecord + str(sh.cell(rx,18).value) + vbtab  # PRIOR_START_DATE_2
            y= str(sh.cell(rx,19).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_END_DATE_2
            else:
                strRecord = strRecord + str(sh.cell(rx,19).value) + vbtab  # PRIOR_END_DATE_2
            y= str(sh.cell(rx,20).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_CONVERSION_FACTOR_2
            else:
                strRecord = strRecord + str(sh.cell(rx,20).value) + vbtab  # PRIOR_CONVERSION_FACTOR_2
            y= str(sh.cell(rx,21).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_START_DATE_3
            else:
                strRecord = strRecord + str(sh.cell(rx,21).value) + vbtab  # PRIOR_START_DATE_3
            y= str(sh.cell(rx,22).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_END_DATE_3
            else:
                strRecord = strRecord + str(sh.cell(rx,22).value) + vbtab  # PRIOR_END_DATE_3
            y= str(sh.cell(rx,23).value)
            if not y: 
                strRecord = strRecord + ' ' + vbtab # PRIOR_CONVERSION_FACTOR_3
            else:
                strRecord = strRecord + str(sh.cell(rx,23).value) + vbtab  # PRIOR_CONVERSION_FACTOR_3
            #--- start date 1
            #x= str(sh.cell(rx,16).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # START_DATE1 conversion
            #--- end date 1
            #x= str(sh.cell(rx,17).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #   y = xlrd.xldate_as_tuple(z1,0)
            #   strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PR_OHP_ELIG_DT conversion
            #--- priority start date 2
            #x= str(sh.cell(rx,18).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # # PRI_START_DATE2 conversion
            #--- priority end date2
            #x= str(sh.cell(rx,19).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #   z1 = 61
            #   y = xlrd.xldate_as_tuple(z1,0)
            #   strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PRI_END_DATE2 conversion
            #strRecord = strRecord + str(sh.cell(rx,20).value) + vbtab  # PRI_CONV_FACT2
            #--- priority start date 3
            #x= str(sh.cell(rx,21).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PRI_START_DATE3 conversion
            #--- pririty end date 3
            #x= str(sh.cell(rx,22).value)
            #z=(x.split(".")[0])
            #z1 = int(z)
            #if z1 < 61:
            #    z1 = 61
            #    y = xlrd.xldate_as_tuple(z1,0)
            #    strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PRI_END_DATE3 conversion
            #strRecord = strRecord + str(sh.cell(rx,23).value) + vbtab  # PRI_CONV_FACT3
    post=str(strRecord)
    post=post.replace("\n","")
    post=post.replace("\r","")
    strRecord = post + "\n"
    if rx > 0:
       f.write(strRecord)

# Refer to docs for more details.
# Feedback on API is welcomed.
f.close()
print "      End of: ", sys.argv[0]
