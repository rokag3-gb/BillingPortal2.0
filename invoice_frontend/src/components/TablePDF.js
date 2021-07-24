import React from 'react';
import { Text, View, StyleSheet } from '@react-pdf/renderer';

const styles = StyleSheet.create({
    container: {

    },
    header: {
        flexDirection: 'row',
        borderBottomWidth: 1,
        borderBottomStyle: 'dashed',
        borderBottomColor: 'grey',
        fontWeight: 'bold'
        
    },
    headerCell: {
        paddingLeft: '5px',
        // textAlign: 'center',
    },
    body: {
        flexDirection: 'row',
    },
    bodyCell: {
        // borderLeftWidth:1,
        paddingLeft: '5px',
    },
    numberCell: {
        // borderLeftWidth:1,
        paddingRight: '5px',
        textAlign: 'right',
    }
})

function TableHeader({ columns, size }) {
    return (
        <View style={styles.header}>
            {columns.map((column, idx) => {
                const inlineStyle = size[idx] ? {width: size[idx]} : {flexGrow: 1}

                return (<Text key={"h" + idx} style={[styles.headerCell, inlineStyle]}>{column}</Text>)
            })}
        </View>
    )
}
function TableRow({ cells, size, border, boldText }) {
    
    return (
        <View style={styles.body}>
            {cells.map((cell, idx) => {
                let mainStyle = styles.bodyCell
                let inlineStyle = size[idx] ? {width: size[idx]} : {flexGrow: 1}
                let output = cell

                if (typeof cell === 'number') {
                   mainStyle = styles.numberCell
                   output = cell.toLocaleString('ko-KR')
                }
                if (border) {
                    inlineStyle = {...inlineStyle, borderBottomWidth: 1, borderBottomColor: '#c2c2c2', borderBottomStyle: 'dotted'}
                }
                if (boldText) {
                    inlineStyle.fontWeight = 'bold'
                }

                return (<Text key={"c" + idx} style={[mainStyle, inlineStyle]}>{output}</Text>)
            })}
        </View>
    )
}

function TablePDF({ columns, rows, size, style, border=false, boldText=false }) {
    if (!rows) {
        const reservedWidth = size ? size.reduce((prv, cur) => prv + cur, 0) : 0
        const tmpStyle = reservedWidth ? {width: reservedWidth} : {flexGrow: 1}

        return (<Text style={tmpStyle}>No Data</Text>)
    }
    
    const columnSize = size ? size : new Array(rows[0].length).fill(0)

    return (
        <View style={[styles.container, style]}>
            {columns && <TableHeader columns={columns} size={columnSize} />}
            {rows.map((row, idx) => (
                <TableRow key={"r"+idx} cells={row} size={columnSize} idx={idx} border={border} boldText={boldText}/>
            ))}
        </View>
    );
}

export default TablePDF;