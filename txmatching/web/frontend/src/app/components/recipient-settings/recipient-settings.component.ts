import { Component, Input } from '@angular/core';
import { RecipientEditable } from '@app/model/RecipientEditable';
import { BloodGroup } from '@app/model';
import { NgModel } from '@angular/forms';
import { formatNumberForPatient, formatYearOfBirthForPatient } from '@app/directives/validators/form.directive';

// TODO improve code: change functions to arrow functions, don't use null values,
// use correct types for variables instead of "any"
@Component({
  selector: 'app-recipient-settings',
  templateUrl: './recipient-settings.component.html',
  styleUrls: ['./recipient-settings.component.scss']
})
export class RecipientSettingsComponent {

  @Input() recipient?: RecipientEditable;
  @Input() showCountryAndMedicalId: boolean = false;
  @Input() showMatchingConditions: boolean = false;
  public allBloodGroups: BloodGroup[] = Object.values(BloodGroup);

  constructor() {
  }

  public formatYearOfBirth(inputValue: NgModel) {
    if (this.recipient) {
      formatYearOfBirthForPatient(inputValue, this.recipient);
    }
  }

  public formatNumber(inputValue: NgModel): void {
    if (!this.recipient) {
      return;
    }

    const newValue = formatNumberForPatient(inputValue, this.recipient);

    switch (inputValue.name) {
      case 'antibodiesCutoff':
        this.recipient.antibodiesCutoff = newValue;
        break;
      case 'previousTransplants':
        this.recipient.previousTransplants = newValue;
        break;
    }
  }
}
