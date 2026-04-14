first of all the data from the excel should be moved to database that is candidate_info table.
Each new entry in the excel should have a entry in the candidate_info table and job_tracker table.
The job type of this entry will come from job master table that is job_type_id. the job type will be mail sent and the job sub type will be documents required. the status will be pending. the action date will be calculated from the excel sheet data of expected date of jaoining which is also there in candidate info table. we need to start sending mail to candidates whosie joining is within next 60 days or less. so the action date will be 60 days before the expected date of joining or less. we need to calculate the action date based on the current date and the expected date of joining. if the current date is less than or equal to 60 days before the expected date of joining then we need to update the action date as same as next date.
this will be done though a scheduler that will run at 10pm IST everyday using a dag in airflow.
if there is any change in any of the row of the excel sheet than same must be updated in the database.

Next we will send an email to the candidate asking for the documents. this will be done though a scheduler that will run at 9AM IST everyday using a dag in airflow.
This mail send will be triggered based on the job tracker table. we will check the job tracker table based on the action date and job type. if the action date is same as current date and job type is mail sent and job sub type is documents required and status is pending then we will send an email to the candidate asking for the documents after approval from the HR. 
the mail id and employment type of the candidate will be there in the candidate_info table.the document type master has the list of documents on the basis of emplyment type. The mail type master has a draft email where in we will fetch the draft email, alter it on the basis of list of documents and update that mail in job tracker table in draft mail column and change the status to mail drafted. 
the hr can see the drafted mail in the dashboard and can approve or reject it. if approved then the mail will be sent to the candidate and the status will be changed to mail sent. if rejected then the status will be changed to mail rejected. HR can also edit the mail and send it. 
once the mail is sent the list of documents which are required will be entered in the document_tracker table with status as pending.
Also we will add a new entry in the job tracker table where job type will be follow up and job sub type will be documents required and status will be pending. Action date will be 2 days after the mail has been sent. 

Now we will check the job tracker table based on the action date and job type. if the action date is same as current date and job type is follow up and job sub type is documents required and status is pending then we will send an email to the candidate asking for the documents after approval from the HR. 
this mail drafting part will also be running from same dag.

Now the next part is of mail reading and analysing.
We will use another scheduler which will run at 9 pm every day using a dag in airflow. this will read all the received emails and figure out the number of distinct candidates have mailed us basis on the CIN which will be there in the subject of the email. 
Note - a candidate can send more than 1 mail for overall documents as the limit for email size is 10 mb. so we need to figure out the number of distinct candidates have mailed us basis on the CIN which will be there in the subject of the email. 
Once we figured out that we received any email from a specific candidate then we disable the follow up mail for that candidate in the job tracker table and change the status to mail received. 
Now we will classify the received emails into two : has attachments or no attachments.
now for the mails which is classified as has attachments, We need to save the documents received from the candidates in a folder basis on the CIN.
We will also make a entry in job tracker with the job type attachments saved.  

Now here we will trigger our agent. This agent will read all the documents received from the candidates and will verify them and also track the status of the documents.
once the documents are saved the agent will read the documents and will check if the documents are valid or not. if the documents are valid then the agent will update the status of the documents in the document_tracker table as verified. if the documents are not valid then the agent will update the status of the documents in the document_tracker table as not verified. 
the agent need to first classify the received documents that is will send these documents to another LLM(nuMarkDown-8B-thinking). it will classify the document type for all the documents. for example if there is some document it will send to another llm and it will classify it as aadhar card or pan card or passport or driving license or educational certificates or employment certificates or resume or offer letter or relieving letter or experience letter or salary slips or bank statements or any other document. 
the agents need to check the name of the candidate in all the documents and date of birth of the candidate in all the documents. 
The agent will also check the overall experience of candidate is matching with the experience mentioned in the candidate_info table in PREVIOUS_EXPERIENCE column. this will be done with the help of relieving letter and experience letters.
once the document is verified the agent needs to rename the documents. if it is any educational certificate then it should be edu_certificate_name, if it is related to previous experience then it should be exp_certificate_name, if it is related to personal details such as aadhar card or pancard then it should pe emp_certificate_name. 
once the documents are verified and renamed the agent will update the status of the documents in the document_tracker table as verified and will also update the document_store_id with the path of the documents. 
it will also segregate the documents in 4 different folders basis on the document name. Employee folder will contain all the documents related to employment, education folder will contain all the documents related to education, personal_details folder will contain all the documents related to personal details and unmatched folder will contain all the documents which are not matched with any of the above categories or the documents which are not verified.

Once this verification is done then agent will perform gap analysis of the documents that is which all documents are received, which all are pending and which all are rejected and update the status of the documents in the document_tracker table as verified, pending or rejected. 
the same will be visible to the HR in the UI. HR will also manually check the documents and can change the status of the documents in the document_tracker table as verified, pending or rejected or not needed as there may be some cases when a specific document is not need for some specific candidate. 
HR will also have a comment/remarks option where in he/she can mention the reason for rejecting or not needed for some specific candidate. 
Based on this gap analysis and the status of both (agent and HR), the agent will draft an email to the candidate asking for the pending documents. This email will be visible to the HR in the UI and HR can approve or reject the email. if approved then the email will be sent to the candidate and the status will be changed to mail sent. if rejected then the status will be changed to mail rejected. HR can also edit the mail and send it. 
the agent will add a entry in the job tracker table once the mail has been sent to candidate, with the job type follow up and job sub type pending documents and status as pending. Action date will be 2 days after the mail has been sent. 

if the candidate doesn't replies within 2 days then a follow up email will be triggered.
after triggering follow up mail we will add a entry in the job tracker again for a new follow up mail. 
We will also trigger a escalation mail to the HR if the candidate does not respond to the follow up mail twice.

Once the candidate uploads all the documents and the status of all the documents in the document_tracker table is verified then the agent will update the status of the documents in the document_tracker table as completed. 
We will now trigger a summary mail to Hr and joining mail to candidate.