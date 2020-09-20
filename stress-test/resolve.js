import http from 'k6/http';
import { check, group } from 'k6';

export let options = {
    scenarios: {
        resolve: {
            executor: 'constant-vus',
            vus: 500,
            duration: '1m',
            exec: 'resolve'
        }
    }
};

var params = {
    'headers': {
        'Content-Type': 'application/json'
    }
};

var service_url = __ENV.SERVICE_URL
var random_portion = __ENV.RANDOM_PORTION
if (!random_portion) {
    // 80% of requests hits 20% of URLs
    random_portion = 5
}

if (!service_url) {
    service_url = 'http://localhost:8080/'
}
var shorten_url = service_url + '/urls';
var shopee_url = 'https://shopee.sg';

const random_short_url = (ts, vu, iter) => `${service_url}${ts}+${vu}+${iter}"}`;

export function setup() {
    let res = http.post(
        shorten_url,
        JSON.stringify({
            'url': shopee_url
        }),
        params
    )
    let short_url = JSON.parse(res.body).short_url;
    let url_parts = short_url.split('/');
    let short_key = url_parts.pop();

    return {
        fixed_short_url: service_url + short_key,
        timestamp: (new Date()).getTime()
    };
}

export function resolve(data) {
    if (__ITER % random_portion === 0) {
        let res = http.get(random_short_url(data.timestamp, __VU, __ITER));
        check(res, {'Not found status': r => r.status == 404});
    } else {
        let res = http.get(data.fixed_short_url);
        check(res, {'resolve OK status': r => r.status == 200});
    }
}

