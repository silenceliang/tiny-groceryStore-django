   /* Add product listener. */
   function selectOnlyThis(e){
    let checkbox = document.getElementsByClassName('product-vip');
    Array.prototype.forEach.call(checkbox, function(ex){
      ex.checked = false;
    });
    e.checked = true;
  };
  /* Only input numeric. */
  function isNumberKey(e){
    let charCode = (e.which) ? e.which:e.keyCode;
    let regex = new RegExp('[0-9]+', 'g');
    return regex.test(String.fromCharCode(charCode));
  };
  /* Reading CSRF token from cookies. */
  function getCookie(c_name){
    if (document.cookie.length > 0){
        let c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1){
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end === -1) c_end = document.cookie.length;
            // unescape (deprecated) ---> decodeURIComponent
            // reference: MDN 
            return decodeURIComponent(document.cookie.substring(c_start,c_end));
        };
    };
    return "";
  };
  /* Delete the selected item in the order list. */
  function AppendDeleteBtnListener(e){
    e.preventDefault();
    e.stopPropagation();
    
    let row = e.target.closest('tr');
    let order_content = {
      'o_id': row.cells[0].textContent,
      'product_id':row.cells[1].textContent,
      'qty':row.cells[2].textContent,
      'action':'del'
    };
    fetch('delFromOrder', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
        'Accept': 'application/json',
      },
      body: JSON.stringify(order_content),
    })
      .then((response) => response.json())
      .then((data) => {
        e.target.closest('tr').remove();
        if(data['notice']){
          alert('Enter the goods ' + data['p_id'] +' from zero to n.');
        };
        let product_table = document.getElementById('prod_tab');
        let pt_nums = product_table.rows.length;
        for (let i = 1; i < pt_nums; ++i){
          let target_prod = product_table.rows[i].cells[0].innerHTML;
          if(target_prod === data['p_id']){
            let ord_num = data['qty'];
            let cur_num = product_table.rows[i].cells[1].innerHTML;
            product_table.rows[i].cells[1].innerHTML = ~~(cur_num) + ~~(ord_num);
            break
          };
        };
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };
  /* Add a product to the oder list. */
  function addProduct(data){
    let field = ['o_id','p_id','qty','price','s_id','c_id'];
    let OrderTable = document.getElementById('ord_tab');
    let ProductTable = document.getElementById('prod_tab');
    let header_counts = OrderTable.rows[0].cells.length;
    let pt_nums = ProductTable.rows.length;
    
    // i from 1 to pt_nums because index 0th represents the header.
    for (let i = 1; i < pt_nums; ++i){
      let target_prod = ProductTable.rows[i].cells[0].innerHTML;
      if(target_prod === data[field[1]]){
        let ord_num = data[field[2]];
        let cur_num = ProductTable.rows[i].cells[1].innerHTML;
        ProductTable.rows[i].cells[1].textContent = cur_num - ord_num;
        break
      }
    }
    let OrderTableTbody = OrderTable.getElementsByTagName('tbody')[0];
    let newRow = OrderTableTbody.insertRow(0);
    for (let i = 0; i < header_counts; ++i){
      let newCell = newRow.insertCell(i);
      let textNode = document.createTextNode(data[field[i]]);
      newCell.appendChild(textNode);
    };
    /* New a button be able to delete this row. */
    let newCell = newRow.insertCell(header_counts);
    let createBtn = document.createElement('button');
    createBtn.classList.add('del-ord');
    let htms = "<svg class='svg-icon' viewBox='0 0 20 20'> \
          <path d='M14.776,10c0,0.239-0.195,0.434-0.435,0.434H5.658c-0.239,0-0.434-0.195-0.434-0.434s0.195-0.434,0.434-0.434h8.684C14.581,9.566,14.776,9.762,14.776,10 M18.25,10c0,4.558-3.693,8.25-8.25,8.25c-4.557,0-8.25-3.691-8.25-8.25c0-4.557,3.693-8.25,8.25-8.25C14.557,1.75,18.25,5.443,18.25,10 M17.382,10c0-4.071-3.312-7.381-7.382-7.381C5.929,2.619,2.619,5.93,2.619,10c0,4.07,3.311,7.382,7.381,7.382C14.07,17.383,17.382,14.07,17.382,10'></path> \
          </svg>";
    createBtn.innerHTML = htms;
    createBtn.onclick = AppendDeleteBtnListener;
    let textNode = document.createTextNode(createBtn);
    newCell.appendChild(createBtn);
  };
  /* initialize all buttons. */
  document.getElementById('add_order').addEventListener("click", function(){
    let selector = document.getElementById('product_select');
    let product_num = document.getElementById('number').value;
    let customer_id = document.getElementById('customer_id').value;
    let vip_or_not = document.getElementById('vip_or_not').checked;
    /* fill the form properly. */
    if(selector.selectedIndex===0 || product_num==="" || customer_id===""){
      alert('Please fill the actual number or select properly.');
      return;
    };
    /* Make sure quantity > 0 */
    if(~~(product_num)<=0){
      alert('Do not input number of quantity less than zero.');
      return;
    }

    let product_vip_or_not = document.getElementsByClassName('product-vip')[selector.selectedIndex-1].checked;
    let data = {
      'product_id': selector.options[selector.selectedIndex].text,
      'qty': product_num,
      'customer_id': customer_id,
      'vip': vip_or_not,
      'prod_vip': product_vip_or_not,
      'action': 'add'
    };

      /* To Send a request to add items to order list. */
    fetch('add2order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
          'Accept': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        if(data['status'])
          addProduct(data);
        else{
          alert(data['message']);
          console.error(data['message']);
        }
      })
      .catch((error) => {
        console.error('Error: ', error);
      });
  });
  
  document.getElementById('find_top3').addEventListener("click",function(){     
    /* To Send a request to add items to order list. */
    fetch('findTop3', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
        'Accept': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((response) => response['results'])
    .then((data) => {
      let res = "";
      console.log('Success:', data);
      for (let i = 0; i < data.length; ++i){
        res += "the top." + i + " product : "  + data[i]['p_id'] + "; total sell volume : " + data[i]['total_sell'] + "<br>";
      };
      document.getElementById('top3_res').innerHTML = res;
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    });
  
  let del_ord_list = document.querySelectorAll('.del-ord');
  Array.from(del_ord_list).forEach(function(e){
    e.addEventListener('click', AppendDeleteBtnListener);
  });
