package com.imhotepisinvisible.sectalkslon0x16;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    TextView mTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        String filename = "flag2";
        FileOutputStream outputStream;

        try {
            outputStream = openFileOutput(filename, Context.MODE_PRIVATE);
            outputStream.write(stringFromJNI1().getBytes());
            outputStream.close();
            Toast.makeText(getApplicationContext(), "File flag2 written to filesystem", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            e.printStackTrace();
        }

        mTextView = (TextView) findViewById(R.id.text);
    }

    public void pressMe(View view) {
        Toast.makeText(getApplicationContext(), "Making HTTP request...", Toast.LENGTH_SHORT).show();
        // Do something in response to button click
        RequestQueue queue = Volley.newRequestQueue(this);
        StringRequest stringRequest = new StringRequest(Request.Method.GET, stringFromJNI2(),
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        mTextView.setText("Response is: "+ response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                mTextView.setText("That didn't work!");
            }
        }){
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("Accept-Language", "fr");
                params.put(stringFromJNI3(), stringFromJNI4());

                return params;
            }
        };

        queue.add(stringRequest);
    }

    // flag{progressive_conductor_emotion}
    public native String stringFromJNI1();

    // http://imhotepisinvisible.com:34567
    public native String stringFromJNI2();

    // X-Admin
    public native String stringFromJNI3();

    // False
    public native String stringFromJNI4();

    static {
        System.loadLibrary("native-lib");
    }
}
