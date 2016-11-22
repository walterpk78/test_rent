
String.prototype.if_empty = function(default_str) {
    return (this.length === 0) ? default_str : this;
};
String.prototype.truncate = function(max_len, end_str) {
    return (this.length >= max_len) ? this.substring(0, max_len - end_str.length) + end_str : this.toString()
};