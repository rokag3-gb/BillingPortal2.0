export function getDateSet(d){
    const now = new Date();
    const from = new Date();
    from.setMonth(now.getMonth() -d)
    from.setDate(1)

    return [from, now]
}

export function getDateFormat(date){
    var year = date.getFullYear();
    var month = ("0" + (1 + date.getMonth())).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);

    return year + "-" + month + "-" + day;
}

export function isEmpty(val){
    return val === undefined || val === null || val === "";
}