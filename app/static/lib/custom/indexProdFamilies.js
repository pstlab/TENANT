// function to execute on page load
$(document).ready(function() {
        
    /**************************************
    *   Submit a product family
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var pfName = document.getElementById('new-pfname').value;
        var defaultP = document.getElementById('new-defaultpf').value;

        if (pfName === "") {
            window.alert("Enter all the information of the product family!");
        }

        else {
            var data = [];
            data.push({'name':pfName, 'defaultp':defaultP});
            data.push('new');
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/products/PF/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/products/PF/");
            });
        }
    });

    /**************************************
    *   Delete a product family
    ***************************************/
    $(".removePF").click(function() {
        var pfId = $(this).siblings(".id").html();
        var tmp = [pfId, 'remove']

        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/products/PF/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/products/PF/");
        });
    });

    /**************************************
    *   Edit a product family
    **************************************/
    // Change the name
    $(".pfname").change(function(){
        //Take the elements
        var pfId = $(this).siblings(".id").html();
        var name = this.value;
        var defProcess = $(this).siblings(".defaultpf")[0].value;

        if (name === "") {
            window.alert("Enter all the information of the product family!");
        }

        else {
            var data = [];
            data.push(pfId);
            data.push({'name':name, 'process':defProcess});
            data.push('edit')
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/products/PF/',
                type : 'post',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function() {
                location.replace("/products/PF/");
            });
        }
    });
    // Change the process
    $(".defaultpf").change(function(){
        //Take the elements
        var pfId = $(this).siblings(".id").html();
        var name = $(this).siblings(".pfname").val();
        var defProcess = this.value;

        if (name === "") {
            window.alert("Enter all the information of the product family!");
        }

        else {
            var data = [];
            data.push(pfId);
            data.push({'name':name, 'process':defProcess});
            data.push('edit')
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/products/PF/',
                type : 'post',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function() {
                location.replace("/products/PF/");
            });
        }
    });
    // Delete a product from the family
     $(".removeP").click(function() {
        var pfId = $(this).parent().siblings('.mainproperties').children(".id").html();
        var prodId = $(this).siblings(".prodid").html();
        var tmp = [];
        tmp.push({'prodFamily':pfId, 'prodId':prodId});
        tmp.push('removeProd')

        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/products/PF/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/products/PF/");
        });
    });
});