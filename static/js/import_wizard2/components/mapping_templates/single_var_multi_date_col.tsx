/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Component for the mapping section for the singleVarMultiDateCol template
 */

import React from "react";

import { isValidDate } from "../../../utils/string_utils";
import { INVALID_DATE_MSG, INVALID_VARIABLE_MSG } from "../../constants";
import { MappingTemplateProps } from "../../templates";
import {
  MAPPED_THING_NAMES,
  MappedThing,
  MappingType,
  MappingVal,
} from "../../types";
import { isValidVariable } from "../../utils/validation";
import { MappingColumnInput } from "../shared/mapping_column_input";
import { MappingConstantInput } from "../shared/mapping_constant_input";
import { MappingHeaderInput } from "../shared/mapping_header_input";
import { MappingPlaceInput } from "../shared/mapping_place_input";

export function SingleVarMultiDateCol(
  props: MappingTemplateProps
): JSX.Element {
  return (
    <div id="single-var-multi-date">
      <MappingConstantInput
        mappedThing={MappedThing.STAT_VAR}
        mappingVal={props.userMapping.get(MappedThing.STAT_VAR)}
        onMappingValUpdate={(
          mappingVal: MappingVal,
          hasInputErrors: boolean
        ): void =>
          props.onMappingValUpdate(
            MappedThing.STAT_VAR,
            mappingVal,
            hasInputErrors
          )
        }
        isRequired={true}
        isValidValue={isValidVariable}
        invalidValueMsg={INVALID_VARIABLE_MSG}
      />
      <MappingPlaceInput
        mappingType={MappingType.COLUMN}
        mappingVal={props.userMapping.get(MappedThing.PLACE)}
        onMappingValUpdate={(mappingVal: MappingVal): void =>
          props.onMappingValUpdate(MappedThing.PLACE, mappingVal, false)
        }
        orderedColumns={props.csvData.orderedColumns}
      />
      <MappingHeaderInput
        mappedThingName={
          MAPPED_THING_NAMES[MappedThing.DATE] || MappedThing.DATE
        }
        mappingVal={props.userMapping.get(MappedThing.DATE)}
        onMappingValUpdate={(
          mappingVal: MappingVal,
          hasInputErrors: boolean
        ): void =>
          props.onMappingValUpdate(MappedThing.DATE, mappingVal, hasInputErrors)
        }
        orderedColumns={props.csvData.orderedColumns}
        isValidHeader={isValidDate}
        invalidHeaderMsg={INVALID_DATE_MSG}
      />
      <MappingColumnInput
        mappedThing={MappedThing.UNIT}
        mappingVal={props.userMapping.get(MappedThing.UNIT)}
        onMappingValUpdate={(mappingVal): void =>
          props.onMappingValUpdate(MappedThing.UNIT, mappingVal, false)
        }
        orderedColumns={props.csvData.orderedColumns}
        isRequired={false}
      />
    </div>
  );
}
