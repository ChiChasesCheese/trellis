# QRN-244: The API falls over during phishing campaigns

During a phishing campaign we get thousands of reports for the same message within minutes, and the API
falls over. Reviewers also want to see how many people reported a message: `GET /reports/<id>` and
`GET /reports` should show it as `reporter_count`.
