function utils_type(obj) {
    const t = typeof obj;
    if(t === 'object' && !Array.isArray(obj)) return 'dict';
    if(t === 'object') return 'array';
    if(t === 'number' && obj % 1 === 0) return 'int';
    if(t === 'number') return 'float';
    if(t === 'string') return 'string';
    return t;
}
function utils_array_length(array) {
    return array.length;
}
function utils_array_clone(array) {
    return [ ...array ];
}
function utils_array_concat(array1, array2) {
    return array1.concat(array2);
}