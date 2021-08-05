import React from 'react';
import TextBox from 'devextreme-react/text-box';
import { Validator, PatternRule } from 'devextreme-react/validator';

function OrgSearchBox({ value, onValueChanged }) {
    return (
        <div style={{paddingLeft: 5}}>
            <TextBox valueChangeEvent="keyup" value={value} onValueChanged={onValueChanged} width={80} placeholder="Org ID">
                <Validator>
                    <PatternRule message="숫자만 입력해주세요." pattern={/^[0-9]*$/} />
                </Validator>
            </TextBox>
        </div>
    )
}

export default OrgSearchBox;