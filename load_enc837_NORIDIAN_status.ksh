#!/bin/ksh

# Do NOT put any code before this line

#########################################################################################
# MODULE NAME:  load_enc837_noridian_staus.ksh
# Description: This script executes a Unix BCP process to load the data from incoming 
#              OHP 837 Status file into the ODS_ENC837_NORIDIAN_RAW table.
#----------------------------------------------------------------------------------------
# Copyright         : (C) 2010 ODS
# Revision          : $Revision: 1.2 $
#----------------------------------------------------------------------------------------
# CHANGE HISTORY
# DATE         NAME        Change Description
#----------------------------------------------------------------------------------------
#########################################################################################

echo 'Starting load_enc837_noridian_status.ksh - $Revision: 1.2 $'
date

###########################################################################
# Argument Handling
###########################################################################
if [[ $# -lt 2 ]]
then
        echo "Error: too few arguments"
        echo "Usage: ./load_enc837_noridian_status.ksh [file_dir] [file_name]"
        return 2
fi


formatfile="${ENV_ROOT_DIR}/prog/clm_encounter_OHP/unx/load_enc837_noridian_status.fmt"
DB_TABLE=${DB_WRK}.dbo.ODS_ENCNOR_NDC_RAW
BASE_ISQL_CMD="isql -S ${DSQUERY} -U ${DBO_USER} -P ${DBO_PASSWORD}"


###########################################################################
# Make sure directory passed in as parameter is valid
###########################################################################

INPUT_DIR=$1

if [ ! -d ${INPUT_DIR} ] ; then
   echo "Cannot find ${INPUT_DIR}!"
   return 3
fi


###########################################################################
# Make sure file passed in as parameter is valid
###########################################################################

INPUT_FILE=$2
INPUT_FILE_DIR=${INPUT_DIR}/${INPUT_FILE}

if [ ! -a ${INPUT_FILE_DIR} ] ; then
   echo "Cannot find ${INPUT_FILE_DIR}!"
   return 3
fi

echo "Input File: ${INPUT_FILE_DIR}"

errorfile="${INPUT_DIR}/load_noridian_status_error.dat"


###########################################################################
# Truncate ODS_ENC837_NORIDIAN_RAW table
###########################################################################

echo "Truncating the work table ${DB_TABLE}"
SETUP_ISQL_CMD="echo 'truncate table ${DB_TABLE}\ngo' | ${BASE_ISQL_CMD}"
eval $SETUP_ISQL_CMD
RET=$?
if [ $RET -ne 0 ]
then
    echo "Error truncating table ${DBTABLE}: isql failed with return value of $RET"
    return $RET
fi


###########################################################################
# Delete old error file, if it is still there from last run
###########################################################################
if [ -e ${errorfile} ] ; then
   echo "Removing old error file '${errorfile}'"
   rm $errorfile
fi


#######################################################################
# BCP IN  *ODS_ENC837_NORIDIAN_RAW TABLE
#######################################################################

echo "Starting bcp of file ${INPUT_FILE_DIR}"
echo "   into table ${DB_TABLE}..."
echo " ******** start bcp *********"
bcp ${DB_TABLE} in ${INPUT_FILE_DIR} -S${DSQUERY} -U${DBO_USER} -P${DBO_PASSWORD} -f$formatfile -e${errorfile} -g 1


#######################################################################
# Error checking for the bcp
#######################################################################

if [ $? -ne 0 ]; then
    echo ' ****** ERROR: bcp failed !! ********* '
    exit 2 
fi    

if [ -e ${errorfile} ] ; then
   echo ' ****** ERROR: bcp failed !! ********* '
   echo "Return code is 2"
   echo ${errorfile}
   exit 2
else
   lnRetCd=$?
   echo 'bcp was successful.'
fi
echo ""
echo " ******** end bcp ***********"



#######################################################################
# Put filename into table records
#######################################################################

echo "Updating table with filename..."
isql -S$DSQUERY -U$DBO_USER -P$DBO_PASSWORD << EOSQL 2>&1 
Use $DB_WRK

DECLARE @create_dt DATETIME

SELECT @create_dt = getdate()

UPDATE $DB_TABLE
SET FILENAME  = '$INPUT_FILE'
   ,CREATE_DT = @create_dt

If @@error <> 0
Begin
    Raiserror 99999
        "An error occurred when updating filename in table"
    Goto ERRORSEQ
End

ERRORSEQ:
GO
EOSQL

if [ $? -ne 0 ]; then
    echo "ERROR: Update filename in table!!!!"
    exit 1
fi    


#######################################################################
# Job successful.
#######################################################################

echo '******* load_noridian_837_status.ksh Job Completed Successfully **********'
date
exit 0
