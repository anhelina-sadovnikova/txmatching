import { Component, Input, OnInit } from '@angular/core';
import { Donor } from '@app/model/Donor';
import { countAllMessages, findMostSevereMessageType, WarningType } from '@app/helpers/messages';

@Component({
  selector: 'app-patient-donor-item',
  templateUrl: './patient-donor-item.component.html',
  styleUrls: ['./patient-donor-item.component.scss']
})
export class PatientDonorItemComponent implements OnInit{

  @Input() item?: Donor;

  public allMessagesCount: number = 0;
  public mostSevereMessageType: WarningType = 'info';

  constructor() {}

  ngOnInit() {
    this.allMessagesCount = countAllMessages(this.item);
    this.mostSevereMessageType = findMostSevereMessageType(this.item);
  }
}
