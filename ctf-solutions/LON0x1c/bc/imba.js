// Either copy the table array or pause execution in dev tools inside the render function
let table = this.table()
let flag_index = Array.from(Array(table.length).keys())
let flag = Array(35)
while(table.length) {
    let i = table[0][0]
    flag[flag_index[i]] = String.fromCharCode(table[0][1])
    flag_index.splice(i,1) // The subpass function
    table = table.slice(1) // The subtable function
}
console.log(flag.join(""))
