import { Component, OnInit } from '@angular/core';
import { FileService } from '../file.service';

@Component({
  selector: 'app-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.scss'],
  providers: [FileService]
})
export class FileComponent implements OnInit {

  constructor(private fileService: FileService) { }

  ngOnInit() {
    this.getFiles()
  }

  public files : any;

  getFiles()  {
    this.fileService.getFiles()
        .toPromise()
        .then(files => this.files = files,
              error => {
                console.log(error);
              });
  }

  delete(hash) {
    if (!confirm("Are you sure?")) {
      return;
    }
    this.fileService.deleteFile(hash)
    this.files = this.files.filter((el) => {
      return el.hash != hash
    })
  }

  sort() {
    var moved = []

    this.fileService.sortFiles()
        .toPromise()
        .then(m => {
                moved = m
              },
              error => {
                console.log(error);
              });
    this.getFiles()
  }
}
