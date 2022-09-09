# Onboarding Guide

## Obtain certificate from secret

Netconf driver certificate is present in the secret netconf-driver-tls. Get the certificate from the secret.

```bash oc get secret netconf-driver-tls -o 'go-template={{index .data "tls.crt"}}' | base64 -d > netconf-tls.pem```

## Onboard NetConf to LM
 
Use the following command to onbaord Netconf driver into CP4NA environment called 'dev01'.

```bash lmctl resourcedriver add --type netconf --url https://netconf-driver:7139 dev01 --certificate netconf-tls.pem```