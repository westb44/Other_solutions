#!/bin/ksh

# Do NOT put any code before this line

#######################################################################
#
#  MODULE NAME:load_999_claims.ksh
#
#  DESCRIPTION: This script executes a Unix BCP process to load the
#  data from incoming 999 Encounter Claims reject files into the
#  ODS_ENC837_RESUB_CLCL table.
#
#     $Revision: 1.2 $
#
#     LANGUAGE: KORN SHELL
#
#---------------------------------------------------------------------
#
#
#=====================================================================
#  MODIFICATION HISTORY
#
#  Date       Chg ID  Developer      Description of Change
#=====================================================================
# 07/13/2012          brownw         CMS   
# 08/02/2012          cavallg        Only process 1 file 
# 08/06/2012          cavallg        Modify commands to strip out claim id into temp table
# 09/25/2012          brownw         Bug 23845 Notes needed for 999 claims re-extract
########################################################################

echo 'Startingload_999_claims.ksh at ' `date`
date

INPUT_DIR=$1
INPUT_FILE=$2


echo "INPUT_DIR     : $INPUT_DIR"
echo "INPUT_FILE    : $INPUT_FILE"
REJECT_FILE="${INPUT_DIR}/reject.txt"
REJECT_FILE2="${INPUT_DIR}/reject2.txt"

###########################################################################
# Make sure directory passed in as parameter is valid
###########################################################################

if [ ! -d ${INPUT_DIR} ] ; then
   echo "Cannot find ${INPUT_DIR}!"
   return 3
fi

###########################################################################
# Delete old error file
###########################################################################
errorfile="${INPUT_DIR}/load_999_status_error.dat"

echo "ERROR FILE    : $errorfile"

if [ -f ${errorfile} ] ; then
   rm $errorfile
   echo "Removed Error File "
fi

###########################################################################
# Make sure file passed in as parameter is valid
###########################################################################
if [ $# -ne 2 ] ; then
   echo "ERROR: Missing required parameter"
   echo "Usage:load_999_claims.ksh directory filename "
   return 3
fi

formatfile="${ENV_ROOT_DIR}/prog/clm_encounter_OHP/unx/load_999_claims.fmt"
DB_TABLE=${DB_WRK}.dbo.ODS_ENC837_RESUB_CLCL
BASE_ISQL_CMD="isql -S ${DSQUERY} -U ${DBO_USER} -P ${DBO_PASSWORD}"

echo "FORMAT FILE   : ${formatfile} "

###########################################################################
# Make sure file passed in as parameter is valid
###########################################################################

INPUT_FILE_DIR=${INPUT_DIR}/${INPUT_FILE}
echo "Input File Dir: '${INPUT_FILE_DIR}'"

errorfile="${INPUT_DIR}/load_999_status_error.dat"

###########################################################################
# Truncate ODS_ENC837_RESUB_CLCL table
###########################################################################

echo "Truncating the work table ${DB_TABLE}"
SETUP_ISQL_CMD="echo 'truncate table ${DB_TABLE}\ngo' | ${BASE_ISQL_CMD}"
eval $SETUP_ISQL_CMD
RET=$?
if [ $RET -ne 0 ] ; then
    echo "Error truncating table ${DBTABLE}: isql failed with return value of $RET"
    return $RET
fi


###########################################################################
# Delete old error file, if it is still there from last run
###########################################################################
echo "Removing old error file ${errorfile}"
if [ -e ${errorfile} ] ; then
   rm $errorfile
   echo "Removed old error file ${errorfile}"
fi
if [ -e ${REJECT_FILE} ] ; then
   rm $REJECT_FILE
   echo "Removed old reject file ${REJECT_FILE}"
fi
if [ -e ${REJECT_FILE2} ] ; then
   rm $REJECT_FILE2
   echo "Removed old reject file ${REJECT_FILE2}"
fi

#######################################################################
# BCP IN  *ODS_ENC837_RESUB_CLCL TABLE
#######################################################################
echo "Starting bcp of files into table '${DB_TABLE}'" 
echo " ******** Start bcp *********"

BCP_INPUT_FILE_TEMP="${INPUT_DIR}/temp_999.txt"
echo "BCP_INPUT_FILE_TEMP : ${BCP_INPUT_FILE_TEMP}"

#######################################################################
if [ -e ${INPUT_FILE_DIR} ] ; then

    BCP_INPUT_FILE="${INPUT_DIR}/load_999_file.txt"
    echo "BCP_INPUT_FILE : ${BCP_INPUT_FILE}"

    $(cat ${INPUT_FILE_DIR}| tail -c80 > ${REJECT_FILE})
    $(awk -F"'" '{ print $1; print $2; print $3; print $4; print $5; print $6; print $7; print $8; print $9; print $10;}' ${REJECT_FILE} > ${REJECT_FILE2})
    reject=$(awk -F~ 'substr($0, 1, 3)=="AK9" {printf ("%s",substr($2,1,1))}' ${REJECT_FILE2})
    #echo "reject 999: ${reject}"
    if [ $reject = '']; then
        reject=R
    fi
    
    tr -s '~' '\n' < ${INPUT_FILE_DIR} |awk -F+ 'substr($0, 1, 5)=="CLM01" { printf ("0~%s~Y~'${reject}'\n",substr($2, 1, 12)) }' > ${BCP_INPUT_FILE_TEMP}
    sort -u ${BCP_INPUT_FILE_TEMP} > ${BCP_INPUT_FILE}
    bcp ${DB_TABLE} in ${BCP_INPUT_FILE} -S${DSQUERY} -U${DBO_USER} -P${DBO_PASSWORD} -f$formatfile -e${errorfile}
    
    if [ -e ${REJECT_FILE} ] ; then
       rm $REJECT_FILE
    fi
    if [ -e ${REJECT_FILE2} ] ; then
       rm $REJECT_FILE2
    fi 
fi

#######################################################################
# Error checking for the bcp
#######################################################################

if [ $? -ne 0 ] ; then
    echo ' ****** ERROR: bcp failed !! ********* '
    exit 2 
fi    

#if [ -e ${errorfile} ] ; then
#   echo ' ****** ERROR: bcp failed !! ********* '
#   echo "Return code is 2"
#   echo ${errorfile}
#   exit 2
#else
#  lnRetCd=$?
#  echo 'bcp was successful.'
#fi
echo ""
echo " ******** end bcp ***********"

#######################################################################
# Job successful.
#######################################################################

echo 'Endingload_999_claims.ksh - $Revision: 1.2 $'
date
exit 0
