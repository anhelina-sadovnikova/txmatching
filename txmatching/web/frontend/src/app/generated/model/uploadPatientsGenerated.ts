/**
 * API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { RecipientInputGenerated } from './recipientInputGenerated';
import { CountryCodeGenerated } from './countryCodeGenerated';
import { DonorInputGenerated } from './donorInputGenerated';


export interface UploadPatientsGenerated { 
    /**
     * If *true* the currently uploaded patients will be added to the patients already in the system. If *false* the data in the system will be overwritten by the currently uploaded data.
     */
    add_to_existing_patients?: boolean;
    country: CountryCodeGenerated;
    donors: Array<DonorInputGenerated>;
    recipients: Array<RecipientInputGenerated>;
    /**
     * The TXM event name has to be provided by an ADMIN.
     */
    txm_event_name: string;
}

