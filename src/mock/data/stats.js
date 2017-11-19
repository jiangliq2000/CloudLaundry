/**
 * Created by jerry on 2017/4/14.
 */

import Mock from 'mockjs'

var template = {
    devid: '11111',
    wash: [{washSum:'10', wash1:'1',wash2:'2', wash3:'3',wash4:'4', wash5:'5',wash6:'6',wash7:'7',wash8:'8'}],
    drug: [{drug1:'100',drug2:'200', drug3:'50', drug4:'60',drug5:'70',drug6:'80',drug7:'90',drug8:'120'}],
    formula: [{fm1:'10',fm2:'20',fm3:'30',fm4:'40',fm5:'50',fm6:'60',fm7:'70',fm8:'80',fm9:'90',fm10:'100',
              fm11:'110',fm12:'120',fm13:'130',fm14:'140',fm15:'150',fm16:'160',fm17:'170',fm18:'180',fm19:'190',fm20:'200'}]
  }


const Stats = []

for(let i=0; i<3; i++){
    Stats.push(template)
}

export {Stats}
