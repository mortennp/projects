#!/bin/sh
location=northeurope
base_name=smillaai
rg_name=$base_name-rg
stor_acct_name=${base_name}blobstor

# az group create --name $rg_name --location $location


# az storage account create --name $stor_acct_name --location $location --resource-group $rg_name --sku Standard_LRS --kind StorageV2 --access-tier Hot
echo $blobStorageAccountKey=$(az storage account keys list -g myResourceGroup -n $blobStorageAccount --query [0].value --output tsv)
echo az storage container create -n images --account-name $blobStorageAccount --account-key $blobStorageAccountKey --public-access off

