import { Component, Input } from '@angular/core';
import { faAngleRight } from '@fortawesome/free-solid-svg-icons';
import { Configuration } from '@app/model/Configuration';
import { UiInteractionsService } from '@app/services/ui-interactions/ui-interactions.service';
import { PatientList } from '@app/model/PatientList';
import { Round } from '@app/model/Round';
import { DonorType } from '@app/model';

@Component({
  selector: 'app-matching-round',
  templateUrl: './matching-round.component.html',
  styleUrls: ['./matching-round.component.scss']
})
export class MatchingRoundComponent {

  @Input() round?: Round;
  @Input() patients?: PatientList;
  @Input() configuration?: Configuration;

  public arrowRight = faAngleRight;

  constructor(private _uiInteractionsService: UiInteractionsService) {
  }

  public setActiveTransplant(id: number): void {
    this._uiInteractionsService.setFocusedTransplantId(id);
  }

  get getRoundTooltip(): string {
    switch(this.round?.donorType) {
      case DonorType.DONOR: return 'Round';
      case DonorType.NON_DIRECTED: return 'Round with non-directed donor';
      case DonorType.BRIDGING_DONOR: return 'Round with bridging donor';
      case undefined: return '';
    }
  }
}
