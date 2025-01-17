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
import { HlaAntibodyGenerated } from './hlaAntibodyGenerated';


export interface AntibodyMatchGenerated { 
    hla_antibody: HlaAntibodyGenerated;
    match_type: AntibodyMatchGeneratedMatchTypeEnum;
}
export enum AntibodyMatchGeneratedMatchTypeEnum {
    Split = 'SPLIT',
    Broad = 'BROAD',
    HighRes = 'HIGH_RES',
    None = 'NONE',
    Undecidable = 'UNDECIDABLE',
    HighResWithSplit = 'HIGH_RES_WITH_SPLIT',
    HighResWithBroad = 'HIGH_RES_WITH_BROAD'
};



