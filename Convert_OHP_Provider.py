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
vbtab = "\t"
for rx in range(sh.nrows):
    if rx > 0:
       if 'Inactive' in sys.argv[1]:
            strRecord = str(sh.cell(rx,0).value) + vbtab               # PR_NPI
            strRecord = strRecord + str(sh.cell(rx,1).value) + vbtab   # PR_TAXONOMY_CD
            strRecord = strRecord + str(sh.cell(rx,3).value) + vbtab   # PR_PRRG_ID
            strRecord = strRecord + "         " + vbtab                # PR_MCTN_ID
            strRecord = strRecord + str(sh.cell(rx,2).value) + vbtab   # PR_NAME
            strRecord = strRecord + str(sh.cell(rx,4).value) + vbtab   # PRTP_ID
            strRecord = strRecord + str(sh.cell(rx,5).value) + vbtab   # PRTP_DESC
            strRecord = strRecord + str(sh.cell(rx,6).value) + vbtab   # SPCD_ID
            strRecord = strRecord + str(sh.cell(rx,7).value) + vbtab   # SPCD_DESC
            strRecord = strRecord + str(sh.cell(rx,9).value) + vbtab   # PRLN_ID
            strRecord = strRecord + str(sh.cell(rx,8).value) + vbtab   # PR_ADDR_CSZ
            strRecord = strRecord + str(sh.cell(rx,10).value) + vbtab  # PR_PHONE
            #--- date - 1
            x= str(sh.cell(rx,11).value)
            z=(x.split(".")[0])
            z1 = int(z)
            if z1 < 61:
               z1 = 61
            y = xlrd.xldate_as_tuple(z1,0)
            strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PR_OHP_ELIG_DT

            # Date - 2
            x= str(sh.cell(rx,12).value)
            z=(x.split(".")[0])
            z1 = int(z)
            if z1 < 61:
               z1 = 61
            y = xlrd.xldate_as_tuple(z1,0)
            strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PR_OHP_TERM_DT

            
            strRecord = strRecord + vbtab                              # RAW_PR_OHP_ELIG_DT
            strRecord = strRecord + vbtab                              # RAW_PR_OHP_TERM_DT
            strRecord = strRecord + " " + vbtab                        # PR_ENRL_ST_CD
            strRecord = strRecord + vbtab                              # ENTRY_DT
       else:
            strRecord = str(sh.cell(rx,0).value) + vbtab               # PR_NPI
            strRecord = strRecord + str(sh.cell(rx,1).value) + vbtab   # PR_TAXONOMY_CD
            strRecord = strRecord + str(sh.cell(rx,3).value) + vbtab   # PR_PRRG_ID
            strRecord = strRecord + "         " + vbtab                # PR_MCTN_ID
            strRecord = strRecord + str(sh.cell(rx,2).value) + vbtab   # PR_NAME
            strRecord = strRecord + str(sh.cell(rx,4).value) + vbtab   # PRTP_ID
            strRecord = strRecord + str(sh.cell(rx,5).value) + vbtab   # PRTP_DESC
            strRecord = strRecord + str(sh.cell(rx,6).value) + vbtab   # SPCD_ID
            strRecord = strRecord + str(sh.cell(rx,7).value) + vbtab   # SPCD_DESC
            strRecord = strRecord + str(sh.cell(rx,9).value) + vbtab   # PRLN_ID
            strRecord = strRecord + str(sh.cell(rx,8).value) + vbtab   # PR_ADDR_CSZ
            strRecord = strRecord + str(sh.cell(rx,10).value) + vbtab  # PR_PHONE
            #strRecord = strRecord + str(sh.cell(rx,11).value) + vbtab # PR_OHP_ELIG_DT
            x= str(sh.cell(rx,11).value)
            z= (x.split(".")[0])
            z1= int(z)
            if z1 < 61:
               z1= 61
            y=xlrd.xldate_as_tuple(z1,0)
            strRecord = strRecord + (str(y[1]) + "/" + str(y[2]) + "/" + str(y[0])) + vbtab # PR_OHP_ELIG_DT
            
            strRecord = strRecord + "12/31/9999" + vbtab               # PR_OHP_TERM_DT
            strRecord = strRecord + vbtab                              # RAW_PR_OHP_ELIG_DT
            strRecord = strRecord + vbtab                              # RAW_PR_OHP_TERM_DT
            strRecord = strRecord + " " + vbtab                        # PR_ENRL_ST_CD
            strRecord = strRecord + vbtab                              # ENTRY_DT

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
