# Cloud Foundry MySQL Test App

This repository contains the code necessary for deploying a test application on Cloud Foundry using a Cloud Foundry-provided MySQL service

## Steps for deploying

1. Target your Cloud Foundry installation:

:  `cf login -a <cf-api-target> -o <org> -s <space>`

2. Identify MySQL Configuration:

```
$ cf marketplace
service          plans               description           broker
mysql            db-small            MySQL                 mysql-broker
```

3. Provision MySQL instance

:  `cf create-service mysql db-small demo-mysql`

4. Deploy application

:  `cf push`

