export class Dests {
    constructor(
        public id: number,
        public zone: string,
        public dfrom: string,
        public dto: string,
        public dest_name: string,
    ){}
}

export class Time {
    constructor(
        public working_day: string,
        public holidays: string,
    ) {}
   
}
