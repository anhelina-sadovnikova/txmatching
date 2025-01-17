import { AfterViewInit, Component, ComponentFactoryResolver, ElementRef, Input, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { matchingBatchSize } from '@app/model/Matching';
import { Configuration } from '@app/model/Configuration';
import { ListItem, ListItemDetailAbstractComponent } from '@app/components/list-item/list-item.interface';
import { ListItemDetailDirective } from '@app/directives/list-item-detail/list-item-detail.directive';
import { scrollableDetailClass } from '@app/services/ui-interactions/ui-iteractions';
import { UiInteractionsService } from '@app/services/ui-interactions/ui-interactions.service';
import { PatientList } from '@app/model/PatientList';
import { TxmEvent } from '@app/model/Event';

@Component({
  selector: 'app-item-list',
  templateUrl: './list-item.component.html',
  styleUrls: ['./list-item.component.scss']
})
export class ListItemComponent implements OnChanges, AfterViewInit {

  @ViewChild('list') list?: ElementRef;
  @ViewChild('detail') detail?: ElementRef;

  @ViewChild(ListItemDetailDirective, { static: true }) listItemDetailHost?: ListItemDetailDirective;

  @Input() items: ListItem[] = [];
  @Input() patients?: PatientList;
  @Input() configuration?: Configuration;
  @Input() defaultTxmEvent?: TxmEvent;

  @Input() saveLastViewedItem: boolean = false;
  @Input() useInfiniteScroll: boolean = true;

  @Input() active?: ListItem;
  public activeItem?: ListItem;
  public displayedItems: ListItem[] = [];

  public activeAlignedTop: boolean = true;
  public activeAlignedBottom: boolean = false;

  public scrollableDetailClass: string = scrollableDetailClass;
  public enableSmoothScroll: boolean = true;

  constructor(private _componentFactoryResolver: ComponentFactoryResolver,
              private _uiInteractionsService: UiInteractionsService) {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.listItemDetailComponent) {
      this._loadDetailComponent();
    }

    if (changes.items) {
      this.items = changes.items.currentValue;
      this._reloadItems();
    }
  }

  ngAfterViewInit(): void {
    this._initAdjustingStylesOnScroll(this.list, this.detail);

    if (this.activeItem) {
      this._scrollToElement(this.activeItem.index);
    }
  }

  public handleItemClick(item: ListItem): void {
    this.enableSmoothScroll = true;
    this.setActive(item);
  }

  public setActive(item: ListItem | undefined): void {

    // return if clicked on the same item
    if (this.activeItem === item) {
      return;
    }

    // deactivate activeItem if there is one
    if (this.activeItem) {
      this.activeItem.isActive = false;
    }

    // activate new item
    this.activeItem = item;
    if (item?.index) {
      item.isActive = true;
      this.activeAlignedTop = true;
      this._loadDetailComponent();
      this._scrollToElement(item.index);

      // save last clicked patient pair
      if (this.saveLastViewedItem && this._uiInteractionsService.getLastViewedItemId() !== item.index) {
        this._uiInteractionsService.setLastViewedPair(item.index);
      }
    }
  }

  public onScrollDown(): void {
    this._addItemsBatchToView();
  }

  public trackListItem(index: number, item: ListItem) {
    return item.index;
  }

  private _scrollToElement(id: number): void {
    const activeElement = document.getElementById(`list-item-${id}`);

    if (!this.list || !activeElement) {
      return;
    }

    const scrollable = this.list.nativeElement;

    // wait for element to have .active class
    setTimeout(() => {
      scrollable.scrollTop = activeElement.offsetTop;
    }, 10); // wait 10ms for execution, see https://stackoverflow.com/a/779785/7169288

    if (this.detail) {
      this.detail.nativeElement.scrollTop = 0;
    }
  }

  private _addItemsBatchToView(): void {
    const start = this.displayedItems.length;
    const end = start + matchingBatchSize;
    const matchingsToPush = this.items.slice(start, end);
    this.displayedItems.push(...matchingsToPush);
  }

  private _initAdjustingStylesOnScroll(list?: ElementRef, detail?: ElementRef): void {
    if (!list || !detail) {
      return;
    }

    const listElement = list.nativeElement;
    const detailElement = detail.nativeElement;

    listElement.addEventListener('scroll', (event: WheelEvent) => {
      this._setAlignment(listElement, detailElement);
    });
  }

  private _setAlignment(listElement: HTMLElement, detailItem: HTMLElement): void {
    const activeItem: HTMLElement | null = listElement.querySelector('.active');
    if (!activeItem) {
      return;
    }

    const {
      borderTopLeftRadius,
      borderBottomLeftRadius,
      borderBottomRightRadius,
      borderTopRightRadius
    } = getComputedStyle(activeItem);
    const offsetValue = borderTopLeftRadius || borderBottomLeftRadius || borderBottomRightRadius || borderTopRightRadius;
    const topOffset = Number(offsetValue.replace(/\D+/g, ''));
    const bottomOffset = Number(offsetValue.replace(/\D+/g, ''));

    const detailClientRect = detailItem.getBoundingClientRect();
    const activeItemClientRect = activeItem.getBoundingClientRect();

    const activeTop = activeItemClientRect.top - topOffset;
    const activeBottom = activeItemClientRect.top + activeItem.offsetHeight + bottomOffset;

    const detailTop = detailClientRect.top + topOffset;
    const detailBottom = detailClientRect.top + detailItem.offsetHeight - bottomOffset;

    this.activeAlignedTop = activeTop <= detailTop;
    this.activeAlignedBottom = activeBottom >= detailBottom;
  }

  private _reloadItems(): void {
    if (this.useInfiniteScroll) {
      this.displayedItems = [];
      this._addItemsBatchToView();
    } else if (!this.displayedItems.length) { // first loading
      this.enableSmoothScroll = false;
      this.displayedItems = this.items;
    }

    // set first or saved item as active if not set from @Input()
    let newActiveItem = this.active;
    if (!this.active) {
      newActiveItem = this.displayedItems[0];
      if (this.saveLastViewedItem && this.items.length) {
        const lastViewedId = this._uiInteractionsService.getLastViewedItemId();
        const foundItem = this.items.find(item => item.index === lastViewedId);
        newActiveItem = foundItem ?? newActiveItem;
      }
    }

    this.setActive(newActiveItem);
  }

  private _loadDetailComponent(): void {
    const activeItem = this.activeItem;
    if (!activeItem?.detailComponent) {
      return;
    }

    const detailComponentFactory = this._componentFactoryResolver.resolveComponentFactory(activeItem.detailComponent);

    if (this.listItemDetailHost) {
      const detailViewContainerRef = this.listItemDetailHost.viewContainerRef;
      detailViewContainerRef.clear();
      const detailComponentRef = detailViewContainerRef.createComponent<ListItemDetailAbstractComponent>(detailComponentFactory);
      detailComponentRef.instance.item = activeItem;
      detailComponentRef.instance.patients = this.patients;
      detailComponentRef.instance.configuration = this.configuration;
      detailComponentRef.instance.defaultTxmEvent = this.defaultTxmEvent;
    }
  }
}
