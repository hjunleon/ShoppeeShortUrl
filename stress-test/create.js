import http from 'k6/http';
import { check } from 'k6';

export let options = {
    scenarios: {
        create: {
            executor: 'constant-vus',
            vus: 30,
            duration: '1m',
            exec: 'create'
        }
    }
};

var params = {
    'headers': {
        'Content-Type': 'application/json'
    }
};

var service_url = __ENV.SERVICE_URL
if (!service_url) {
    service_url = 'http://localhost:8080/'
}
const shorten_url = service_url + 'urls';

const payload = (ts, vu, iter) => `{"url":"https://shopee.sg/search?keyword=${ts}+${vu}+${iter}"}`;

export function setup() {
    return { timestamp: (new Date()).getTime() }
}

export function create(data) {
    let res = http.post(
        shorten_url,
        payload(data.timestamp, __VU, __ITER),
        params
    );
    check(res, { 'create OK status': r => r.status == 200 });
}

