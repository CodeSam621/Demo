
## Query to test the Sumologic connetion

```
{
	"attachments": [
		{
			"pretext": "{{TriggerType}} Alert: {{AlertName}}",
			"fields": [
				{
					"title": "Alert URL",
					"value": "{{AlertResponseURL}}"
				},
				{
					"title": "Description",
					"value": "{{Description}}"
				},
				{
					"title": "Trigger Time",
					"value": "{{TriggerTime}}"
				},
				{
					"title": "Time Range",
					"value": "{{TriggerTimeRange}}"
				},
				{
					"title": "Trigger Condition",
					"value": "{{TriggerCondition}}"
				},
				{
					"title": "Trigger Value",
					"value": "{{TriggerValue}}"
				},
				{
					"title": "Query",
					"value": "<{{QueryURL}} | {{Query}}>"
				}
			],
			"mrkdwn_in": ["text", "pretext"],
			"color": "#29A1E6"
		}
	]
}
```

## Sample Payload template
```
{
  "attachments":[{
    "pretext":"Sumo Logic Alert: *{{SearchName}}*",
    "fields":[{
      "title":"Alert URL",
      "value":"{{AlertResponseURL}}"
    },{
      "title":"Description",
      "value":"{{SearchDescription}}"
    },{
      "title":"Query",
      "value":"<{{SearchQueryUrl}} | {{SearchQuery}}>"
    },{
      "title":"Time Range",
      "value":"{{TimeRange}}"
    }],
    "mrkdwn_in":["text","pretext"],
    "color":"#29A1E6"
  }]
}
```

# Sumologic Query

```
// change the _sourceCategory and filter (eg: "Error") as per your logs
_sourceCategory="dev/test-app"
AND "Error"
| formatDate(_receiptTime, "yyyy-MM-dd") as date
| count date

```
