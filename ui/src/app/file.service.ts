import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http'
import 'rxjs/Rx'

@Injectable()
export class FileService {

  constructor(private http: Http) { }

  getFiles() {
    let headers = new Headers();
    headers.append('Accept', 'application/json');
    let url = '/unsorted'

    return this.http
      .get(url, { headers })
      .map(res => res.json())
      .map((res) => {
        return res;
      });
  }

  deleteFile(hash) {
    let headers = new Headers();
    headers.append('Accept', 'application/json');
    let url = `/delete/${hash}`

    return this.http
      .delete(url, { headers })
      .subscribe(res => {
            return res;
      });
  }

  sortFiles() {
    let headers = new Headers();
    headers.append('Accept', 'application/json');
    let url = '/sort'

    return this.http
      .post(url, '', { headers })
      .map(res => res.json())
      .map((res) => {
        return res;
      });
  }
}
