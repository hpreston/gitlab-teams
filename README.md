# gitlab-teams

webhook endpoint for gitlab + cisco webex teams

Full documentation on gitlab webhooks are available [here](https://docs.gitlab.com/ce/user/project/integrations/webhooks.html)

# Installation

### From Source

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Using Docker

```
docker run -p 5000:5000 gitlab-teams
```

```
docker build -t gitlab-teams .
docker run -d -p 5000:5000 \
  --name gitlab-teams \
  -e SPARK_ACCESS_TOKEN=$SPARK_ACCESS_TOKEN \
  -e SPARK_ROOM=$SPARK_ROOM \
  gitlab-teams
```


# Configuration

You can now configure gitlab to send webhook events to the machine you installed
the receiver on.  

Currently only the following events are supported:

* Push
* issues
* pipeline events
* build events
* comment events
* merge request events
