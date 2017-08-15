#!/usr/bin/ksh

# $Id: email_dco_results.ksh,v 1.1 2013/11/13 19:56:21 brownw Exp $
#
# This script runs a stored procedure and emails the results.
#

# Pull in general helper functions.
. $ENV_ROOT_DIR/prog/clm_encounter_OHP/unx/shared_functions.ksh


#
# Argument handling
#
if [[ $# -lt 4 ]]
then
 echo "Error: too few arguments"
 echo "Usage: ./email_sproc_results.ksh SUBJECT_LINE EMAIL_LIST_CODE SPROC_NAME [SPROC_ARGS]"
 echo "              SUBJECT_LINE: Text as it should be in the e-mail subject line"
 echo "           EMAIL_LIST_CODE: E-mail address list code from CTS table ODS_CTS_DSTX_EMAIL_LISTS"
 echo "                SPROC_NAME: Name of stored proc to run.  The output of this stored proc will be sent in the email body"
 echo "                 SPROC_ARG: Optional.  Stored proc arguments"
 return 2
fi

MAIL_SUBJECT_LINE=$1
EMAIL_LIST_CODE=$2
SPROC_NAME=${DB_WRK}.dbo.$3
INDICATOR=$4
shift
shift
SPROC_ARGS=$@

#
# Setup
#

if [ -z "$MAIL_SUBJECT_LINE" ]
then
 MAIL_SUBJECT_LINE="Results of automated '${SPROC_NAME}' run"
fi


#
# Figure out the email recipients
#
MAIL_ADDRESSES=`get_email_addresses $EMAIL_LIST_CODE`
if [ $? -ne 0 ]
then
 echo "Error: couldn't get email addresses for list code ${EMAIL_LIST_CODE}."
 return 2
fi


#
# Run the stored procedure
#
SPROC_RESULT=`run_sql ${SPROC_NAME} ${INDICATOR} `
RET=$?
MAIL_BODY="${SPROC_RESULT}"
if [ $RET -ne 0 ]
then
 MAIL_BODY="${MAIL_BODY}\n\nError: stored procedure run produced the error code $RET"
 SCRIPT_SHOULD_FAIL=yes
fi

print "The following message was e-mailed to ${MAIL_ADDRESSES}:"
print " "
echo "${MAIL_BODY}"

#
# Send the email
#
echo "${MAIL_BODY}" | mail -s "${MAIL_SUBJECT_LINE}" ${MAIL_ADDRESSES}
if [ $? -ne 0 -o -n "$SCRIPT_SHOULD_FAIL" ]
then
 return 2
fi
