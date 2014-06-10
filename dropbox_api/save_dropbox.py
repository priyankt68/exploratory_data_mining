
import dropbox

# YOu can get this from Dropbox developer website for your developer account.
app_key = 'xx'
app_secret = 'xx'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# User authentication
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" after loggin in'
print '3. Copy the authorization code.'
code = raw_input("Enter authorization code here: ").strip()


access_token, user_id = flow.finish(code)

client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

f = open('working-file.txt', 'rb')
response = client.put_file('/gridle_sample_test.txt', f)
print 'uploaded: ', response

folder_metadata = client.metadata('/')
print 'metadata: ', folder_metadata

f, metadata = client.get_file_and_metadata('/gridle_sample_test.txt')
out = open('gridle_sample_test', 'wb')
out.write(f.read())
out.close()
print metadata
