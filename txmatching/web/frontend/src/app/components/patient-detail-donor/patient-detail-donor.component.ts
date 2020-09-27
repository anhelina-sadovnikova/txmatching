import { Component, Input, OnInit } from '@angular/core';
import { ListItemDetailAbstractComponent } from '@app/components/list-item/list-item.interface';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { hlaFullTextSearch } from '@app/directives/validators/configForm.directive';
import { Antigen, Donor, PatientList } from '@app/model/Patient';
import { PatientService } from '@app/services/patient/patient.service';
import { ENTER, SPACE } from '@angular/cdk/keycodes';

@Component({
  selector: 'app-patient-detail-donor',
  templateUrl: './patient-detail-donor.component.html',
  styleUrls: ['./patient-detail-donor.component.scss']
})
export class PatientDetailDonorComponent extends ListItemDetailAbstractComponent implements OnInit {

  @Input() patients?: PatientList;
  @Input() item?: Donor;

  public inputControl: FormControl = new FormControl('');
  public allAntigens: Antigen[] = [];

  public filteredCodes: Observable<Antigen[]>;
  public separatorKeysCodes: number[] = [ENTER, SPACE];

  public loading: boolean = false;
  public success: boolean = false;

  constructor(private _patientService: PatientService) {
    super(_patientService);

    this.filteredCodes = this.inputControl.valueChanges.pipe(
      startWith(undefined),
      map((code: string | null) => code ? hlaFullTextSearch(this.availableCodes, code) : this.availableCodes.slice()));
  }

  ngOnInit(): void {
    this._initAvailableCodes();
  }

  get selectedCodes(): Antigen[] {
    return this.item ? this.item.parameters.hla_typing.hla_types_list : [];
  }

  get availableCodes(): Antigen[] {
    return this.allAntigens.filter(code => !this.selectedCodes.includes(code));
  }

  public addNewAntigen(code: string, control: HTMLInputElement): void {
    if (!this.item || !code.length) {
      return;
    }

    const formattedCode = code.trim().toUpperCase();
    this.item.parameters.hla_typing.hla_types_list.push({ raw_code: formattedCode });

    // reset input
    this.inputControl.reset();
    control.value = '';
  }

  public remove(code: Antigen): void {
    if (!this.item) {
      return;
    }

    const index = this.item.parameters.hla_typing.hla_types_list.indexOf(code);

    if (index >= 0) {
      this.item.parameters.hla_typing.hla_types_list.splice(index, 1);
    }
  }

  public handleSave(): void {
    if (!this.item) {
      return;
    }

    this.loading = true;
    this.success = false;
    this._patientService.saveDonor(this.item)
    .then(() => {
      this.loading = false;
      this.success = true;
    })
    .catch(() => this.loading = false);
  }

  private _initAvailableCodes(): void {
    if (!this.patients || !this.patients.donors) {
      return;
    }

    const allCodes = [];
    for (const d of this.patients.donors) {
      allCodes.push(...d.parameters.hla_typing.hla_types_list);
    }

    this.allAntigens = [...new Set(allCodes)]; // only unique
  }
}
