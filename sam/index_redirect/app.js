'use strict';
exports.handler = (event, context, callback) => {
    const request = event.Records[0].cf.request;

    const olduri = request.uri;

    // 末尾が/で終わっている場合はindex.htmlを付与してリクエスト
    const newuri = olduri.replace(/\/$/, '\/index.html');

    // S3へのリクエストのURLを差し替える
    request.uri = newuri;

    return callback(null, request);
};