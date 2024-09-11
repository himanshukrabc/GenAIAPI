import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css'],
  imports: [CommonModule]
})
export class CardComponent implements OnInit {

  @Input() messagePayload: any;
  @Output() cardEvent = new EventEmitter<any>();

  constructor() { }

  ngOnInit(): void {
  }

  onActionClick(action: any) {
    this.cardEvent.emit(action);
  }

}
