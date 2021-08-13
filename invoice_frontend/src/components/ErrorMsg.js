import React from 'react';

function Status4xx({ status }) {
    return (
        <>
            잘못된 요청입니다.({status})
        </>
    )
}

function Status5xx({ status }) {
    return (
        <>
            잘못된 접근입니다.({status})
        </>
    )
}

function ErrorMsg({ status }) {
    const range = parseInt(status/100)

    
    if (range === 4) {
        return <Status4xx status={status} />
    } else if (range === 5) {
        return <Status5xx status={status} />
    }

    return (
        <>
            에러 입니다 ({status})
        </>
    )

}

export default ErrorMsg;