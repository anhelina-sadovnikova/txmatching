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
import { HlaTypeGenerated } from './hlaTypeGenerated';
import { HlaCodesInGroupsGenerated } from './hlaCodesInGroupsGenerated';


export interface HlaTypingGenerated { 
    /**
     * hla types split to hla groups
     */
    hla_per_groups: Array<HlaCodesInGroupsGenerated>;
    hla_types_list: Array<HlaTypeGenerated>;
}
