import subprocess as sub
import importlib
import os
import shutil
import sys
import time

#####################################################################################
class JobRecord:
  def __init__(self):
    self.queue_id=[]
    

#####################################################################################
class LocalSubmitter:
  """Abstract submission class. Child classes must define:
  __init__: 
     can have any parameters, but should set up any variables like queue time and number of
     processor cores
  _job_status(self,
              queue_id : a string that identifies the queue id of the job
              )
  _submit_job(self,
              inpfns : list of input filenames (list of strings)
              outfn  : where stdout should be sent (string)
              jobname : job name for the queue (string)
              loc :  directory where job should be run (string)
            )
            returns a list of queue ids (list of strings)
  """
  #---------------------------------------------------  
  def execute(self,job_record,dependencies,inpfns,outfn,name):
    """Generate qsub file for this job, run it, and return qid from qsub
    transaction. 
    Adds a an element in job_record['control']['queue_id'] with the queue id
    qid: is a list
    """
    qid = self._submit_job(
        inpfns,
        outfn = outfn,
        jobname = 'crystalrun',
        loc = os.getcwd()
      )
    for q in qid:
      job_record.queue_id.append([name,q])
    return qid
  #---------------------------------------------------
  def status(self,job_record,name):
    """ Returns a list of job status elements """
    status=[]
    for q in job_record.queue_id:
      if q[0]==name:
        status.append(self._job_status(q[1]))
    return status
  #---------------------------------------------------
  def transfer_output(self,job_record,outfiles):
    pass # Files should be already available locally.
  #---------------------------------------------------
  def cancel(self, queue_id):
    output = []
    for q_id in queue_id:
      output.append(self._job_cancel(q_id))

  #-------------------------------------------------------
  def _job_status(self,queue_id):
    return "unknown"
  #-------------------------------------------------------
  def _job_cancel(self,queue_id):
    # Should we raise NotImplemetedError, and catch?
    print("Cancel was called, but not implemented")
  #-------------------------------------------------------
  def _qsub(self,exe,prep_commands=[],final_commands=[],
      name="",stdout="",loc=""):
    """ Helper function for executable submitters. 
    Should work in most cases to simplify code."""

    if stdout=="": stdout="stdout"
    if loc=="": loc=os.getcwd()
    if name=="": name=stdout
    header = []
    exeline = exe
    commands = header +  prep_commands + [exeline] + final_commands

    outstr = ""
    for c in commands:
      # Problem: this method doesn't allow you to watch it's progress.
      outstr+=sub.check_output(c,shell=True).decode()
    with open(stdout,'w') as outf:
      outf.write(outstr)
    return []
      