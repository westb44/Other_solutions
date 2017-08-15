#!/usr/bin/ksh

# Do NOT put any code before this line

#######################################################################
#
#  MODULE NAME: load_enc_835_claims.ksh
#
#  DESCRIPTION: This script executes a Unix BCP process to load the
#  data from incoming OHP Encounter Claims 835 files into the
#  ODS_ENC835_CLAIM_RAW table and inserts a batch record in ODS_ENC835_BATCH
#     $Revision: 1.3 $
#     LANGUAGE: KORNSHELL
#---------------------------------------------------------------------
# INSTALLATION: MODA
#=====================================================================
#  MODIFICATION HISTORY
#
#  Date       Chg ID    Developer      Description of Change
#=====================================================================
# 10/24/2013    brownw    Initial Creation Bug 29310 DCO 837 Conversion
# 04/04/2014    brownw    Bug 31327 fixed processing of multple 835 files.
######################################################################

########################################################################
# I did this because I had trouble with special character ($)  in my password
##########################################################################
CLEAN_PWD=$(echo $DBO_PASSWORD | sed 's/\$/\\$/g')

echo 'Starting load_enc_835_claims.ksh at ' `date`
date

INPUT_DIR=$1

#echo "INPUT_DR        : $INPUT_DIR"

###########################################################################
# Delete old error file
###########################################################################
errorfile="${INPUT_DIR}/load_enc_835_claims_error.dat"

if [ -f ${errorfile} ] ; then
   rm $errorfile
fi

###########################################################################
# Truncate ODS_ENC835_CLAIM_RAW table.
###########################################################################

table1=${DB_WRK}.dbo.ODS_ENC835_CLAIM_RAW
BASE_ISQL_CMD="isql -S ${DSQUERY} -U ${DBO_USER} -P ${CLEAN_PWD}"

    SETUP_ISQL_CMD="echo 'truncate table ${table1}\ngo' | ${BASE_ISQL_CMD}"
    
    eval $SETUP_ISQL_CMD
    RET=$?
    if [ $RET -ne 0 ] ; then
        echo "Error: isql failed with return value of $RET"
        return $RET
    fi
    echo "Table ${table1} truncated"
    
######getting the batch ID set 1 time for all the 835 transactions processed for DCO's######
ISQL_STR="isql -S ${DSQUERY} -U ${DBO_USER} -P ${CLEAN_PWD}"
ISQL_BATCH_CMD="echo 'set nocount on\ngo\nselect ISNULL(MAX(BATCH_ID),0) + 1  from ${DB_WRK}.dbo.ODS_ENC835_BATCH \ngo' | ${ISQL_STR}  -b"
BATCH_ID=`eval ${ISQL_BATCH_CMD}`

#######################################################################
# Insert into Batch table
#######################################################################

isql -S ${DSQUERY} -U ${DBO_USER} -P ${DBO_PASSWORD} << EOSQL 2>&1 

DECLARE @create_dt DATETIME
	
SELECT @create_dt = getdate()

INSERT INTO ${DB_WRK}.dbo.ODS_ENC835_BATCH
(BATCH_ID, FILE_NAME, INTERCHANGE_DT, FILE_ICN, 
ARCHIVE_DT, STATUS, CREATE_DT, UPDATE_DT) 
VALUES
(${BATCH_ID}, '${INPUT_FILE}',  '${BATCH_DT}', 
 '${BATCH_FILE_ICN}',  '1/1/1753',  'Loaded 835 data', 
 @create_dt, @create_dt )

If @@error <> 0
Begin
    Raiserror 99999
        "An error occurred while inserting into batch table"
    Goto ERRORSEQ
End

ERRORSEQ:
GO
EOSQL

if [ $? -ne 0 ]; then
    exit 1
fi    

#while loop for loading all the files.
while [ -e ${INPUT_DIR}/*.835 ]
do
###########################################################################
# Find Oldest
###########################################################################

cd ${INPUT_DIR}
OLDEST_FILE=`ls -1t *.835|tail -1`
#echo "OLDEST FILE: ${OLDEST_FILE}"

if [ -z "$OLDEST_FILE" ]
then
     #echo "no files left to process"
     exit 0
else
    echo "Processing oldest file: $OLDEST_FILE"
fi 

INPUT_FILE_DIR=${INPUT_DIR}/${OLDEST_FILE}
formatfile="${ENV_ROOT_DIR}/prog/clm_encounter_OHP/unx/load_enc_835_claims.fmt"

#echo "Input File: ${INPUT_FILE_DIR}"
echo ""

##########################################################################

BATCH_DT=`awk -F* 'substr($0, 1, 3)=="ISA" { print $10 }' ${INPUT_FILE_DIR}`
BATCH_TIME=`awk -F* 'substr($0, 1, 3)=="ISA" { print $11 }' ${INPUT_FILE_DIR}`
BATCH_FILE_ICN=`awk -F* 'substr($0, 1, 3)=="ISA" { print $14 }' ${INPUT_FILE_DIR}`

#echo ${BATCH_ID}
#echo ${BATCH_DT}
#echo ${BATCH_TIME}
#echo ${BATCH_FILE_ICN}

##########################################################################
# Clean  835 - replace ~ with \n and pick out the required columns from CLP
##########################################################################

BCP_INPUT_FILE="${INPUT_DIR}/CLP_ONLY.txt"

tr '~' '\n' < ${INPUT_FILE_DIR} |  awk -F* -vbatch="$BATCH_ID" 'substr($0, 1, 3)=="CLP" { printf ("%d\t%s\t%s\t%f\t%s\n",batch,$2,$3,$4,$8) }'  > ${BCP_INPUT_FILE}

echo ""

#######################################################################
# BCP IN  *ODS_ENC835_CLAIM_RAW TABLE
#######################################################################

echo " ********   Start BCP into table ${table1} *********"

bcp ${table1} in ${BCP_INPUT_FILE} -S${DSQUERY} -U${DBO_USER} -P${DBO_PASSWORD} -f$formatfile -e${errorfile} -g 1 -Q

#echo "*** DSQUERY ${DSQUERY}"


#######################################################################
# Error checking for the BCP.
#######################################################################

if [ -e ${errorfile} ] ; then
   echo ' ****** Unable to bulk copy the table ODS_ENC835_CLAIM_RAW ********* '
   echo "Return code is 2"
   echo ${errorfile}
   exit 2
else
   lnRetCd=$?
   echo ' *********  End BCP  *************'
   echo ''

fi

mv -f ${INPUT_DIR}/${OLDEST_FILE} ${INPUT_DIR}/arc/${OLDEST_FILE}_`date +"%Y%m%d%H%M"`.sav

done

#######################################################################
# Job successful.
#######################################################################

echo 'Ending load_enc_835_claims.ksh - $Revision: 1.3 $'
date
exit 0
