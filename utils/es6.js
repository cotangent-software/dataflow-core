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
function utils_array_index_of(array, search) {
    return array.indexOf(search);
}
function utils_array_slice(array, slice_start, slice_stop, slice_step) {
    const s = array.slice(slice_start ? slice_start : undefined, slice_stop ? slice_stop : undefined);
    if(!slice_step) {
        return s;
    }
    const stepped = [];
    for(let i=0; i<s.length; i+= slice_step) {
        stepped.push(s[i]);
    }
    return stepped;
}